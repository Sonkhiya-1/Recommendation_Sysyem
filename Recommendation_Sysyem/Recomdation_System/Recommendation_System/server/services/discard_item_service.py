import logging
from server.sentiment_analysis import SentimentAnalysis
from queries.discard_item_queries import get_discard_list, delete_menu_item

class DiscardItemService:
    def __init__(self, db, notification_service):
        self.db = db
        self.notification_service = notification_service

    def view_discard_list(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            discard_list = get_discard_list(cursor)

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
            delete_menu_item(cursor, item_id)
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
