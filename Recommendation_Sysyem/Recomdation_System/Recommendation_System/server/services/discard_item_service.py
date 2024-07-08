import logging
from server.sentiment_analysis import SentimentAnalysis

class DiscardItemService:
    def __init__(self, db, notification_service):
        self.db = db
        self.notification_service = notification_service

    def view_discard_list(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT mi.id, mi.name, mi.average_rating, 
                       GROUP_CONCAT(DISTINCT f.comment SEPARATOR '; ') as sentiments
                FROM menu_items mi
                LEFT JOIN feedback f ON mi.id = f.menu_item_id AND f.sentiment = 'negative'
                WHERE mi.average_rating < 2
                GROUP BY mi.id, mi.name, mi.average_rating
            """)
            discard_list = cursor.fetchall()

            for item in discard_list:
                comments = item['sentiments'].split('; ') if item['sentiments'] else []
                sentiments = set()
                for comment in comments:
                    sentiment_type, sentiment_words = SentimentAnalysis.analyze(comment)
                    if sentiment_type == 'negative':
                        sentiments.update(sentiment_words)
                item['sentiments'] = ', '.join(sentiments)
            
            logging.debug(f"Discard list: {discard_list}")
            return {'status': 'success', 'discard_list': discard_list}
        except Exception as e:
            logging.error(f"Error in view_discard_list: {e}")
            return {'status': 'error', 'message': f'Failed to retrieve discard list: {str(e)}'}



    def remove_menu_item(self, request, client_socket):
        if request.get('role') not in [1, 2]:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            item_id = request['item_id']
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
            self.db.commit()
            logging.debug(f"Menu item {item_id} removed from menu.")
            return {'status': 'success', 'message': 'Menu item removed'}
        except Exception as e:
            logging.error(f"Error in remove_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to remove menu item'}

    def request_detailed_feedback(self, request, client_socket):
        if request.get('role') not in [1, 2]: 
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            item_id = request['item_id']
            questions = [
                f"What didn’t you like about {item_id}?",
                f"How would you like {item_id} to taste?",
                "Share your mom’s recipe"
            ]
            message = f"We are trying to improve your experience with {item_id}. Please provide your feedback and help us."
            for question in questions:
                message += f"\n{question}"
            self.notification_service.send_notification_to_all_employees(message)
            logging.debug(f"Requested detailed feedback for menu item {item_id}.")
            return {'status': 'success', 'message': 'Detailed feedback requested'}
        except Exception as e:
            logging.error(f"Error in request_detailed_feedback: {e}")
            return {'status': 'error', 'message': 'Failed to request detailed feedback'}
