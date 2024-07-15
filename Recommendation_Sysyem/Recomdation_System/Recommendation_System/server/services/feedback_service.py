import logging
from server.sentiment_analysis import SentimentAnalysis
from queries.feedback_queries import insert_feedback, get_feedback_counts, update_average_rating

class FeedbackService:
    def __init__(self, db):
        self.db = db

    def send_feedback(self, request, client_socket):
        return self._handle_feedback(request, action="send")

    def submit_feedback(self, request, client_socket):
        return self._handle_feedback(request, action="submit")

    def _handle_feedback(self, request, action):
        try:
            user_id = request['user_id']
            comment = request['comment']
            item_id = request['item_id']
            
            sentiment_type, _ = SentimentAnalysis.analyze(comment)
            
            logging.debug(f"Analyzing feedback: user_id={user_id}, comment='{comment}', sentiment='{sentiment_type}', item_id={item_id}")
            
            cursor = self.db.cursor()
            insert_feedback(cursor, user_id, comment, sentiment_type, item_id)
            self.db.commit()

            self.update_average_rating(item_id)
            
            logging.debug(f"Inserted feedback for menu_item_id {item_id}: {comment}")
            
            return {'status': 'success', 'message': f'Feedback {action}ed'}
        except Exception as e:
            logging.error(f"Error in {action}_feedback: {e}")
            return {'status': 'error', 'message': f'Failed to {action} feedback'}

    def update_average_rating(self, item_id):
        try:
            cursor = self.db.cursor(dictionary=True)
        
            feedback_counts = get_feedback_counts(cursor, item_id)
            logging.debug(f"Feedback counts for item_id {item_id}: {feedback_counts}")
            
            total_feedback = sum(f['count'] for f in feedback_counts)
            if total_feedback == 0:
                logging.debug(f"No feedback available for menu_item_id: {item_id}")
                return

            total_rating = 0
            sentiment_values = {
                'positive': 5,
                'neutral': 3,
                'negative': 1
            }

            for feedback in feedback_counts:
                sentiment = feedback['sentiment']
                count = feedback['count']
                total_rating += sentiment_values.get(sentiment, 3) * count 

            avg_rating = total_rating / total_feedback
            logging.debug(f"Computed average rating for menu_item_id {item_id}: {avg_rating}")

            update_average_rating(cursor, item_id, avg_rating)
            self.db.commit()
            logging.debug(f"Updated average rating for menu_item_id {item_id} to {avg_rating}")
        except Exception as e:
            logging.error(f"Error in update_average_rating: {e}")

    def send_report(self, request, client_socket):
        try:
            report = request['report']
            logging.debug(f"Report received: {report}")
            return {'status': 'success', 'message': 'Report sent successfully'}
        except Exception as e:
            logging.error(f"Error in send_report: {e}")
            return {'status': 'error', 'message': 'Failed to send report'}
