import logging
from server.sentiment_analysis import SentimentAnalysis
from server.services.feedback.feedback_queries import insert_feedback, get_feedback_counts, update_average_rating, insert_feedback_response, get_feedback_questions, get_feedback_responses

class FeedbackService:
    def __init__(self, db, notification_service):
        self.db = db
        self.notification_service = notification_service

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
        
    

    def request_detailed_feedback(self, request, client_socket):
        if request.get('role') not in [1, 2]: 
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            item_id = request.get('item_id')
            if item_id is None:
                raise ValueError("Missing item_id in request")

            cursor = self.db.cursor(dictionary=True)
            feedback_questions = get_feedback_questions(cursor)

            # Send notification to all employees
            notification_message = f"Please provide detailed feedback for menu item ID {item_id}."
            self.notification_service.send_notification_to_all_employees(notification_message)
            self.db.commit()

            logging.debug(f"Requested detailed feedback for item_id {item_id}")
            return {'status': 'success', 'message': 'Feedback request sent to all employees'}
        except Exception as e:
            logging.error(f"Error in request_detailed_feedback: {e}")
            return {'status': 'error', 'message': f'Failed to request detailed feedback: {str(e)}'}
        
        

    def get_feedback_questions(self, request, client_socket):
        if request.get('role') != 3:  # Only employees can respond to feedback
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            cursor = self.db.cursor(dictionary=True)
            feedback_questions = get_feedback_questions(cursor)
            logging.debug(f"Fetched feedback questions: {feedback_questions}")
            return {'status': 'success', 'feedback_questions': feedback_questions}
        except Exception as e:
            logging.error(f"Error in get_feedback_questions: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve feedback questions'}
        
        

    def submit_feedback_response(self, request, client_socket):
        try:
            user_id = request['user_id']
            question_id = request['question_id']
            response = request.get('response', 'Skipped')
            cursor = self.db.cursor()
            insert_feedback_response(cursor, user_id, question_id, response)
            self.db.commit()
            logging.debug(f"Inserted feedback response for question_id {question_id}: {response}")
            return {'status': 'success', 'message': 'Feedback response submitted'}
        except Exception as e:
            logging.error(f"Error in submit_feedback_response: {e}")
            return {'status': 'error', 'message': 'Failed to submit feedback response'}
        
        

    def view_feedback_responses(self, request, client_socket):
        if request.get('role') not in [1, 2]:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            cursor = self.db.cursor(dictionary=True)
            feedback_responses = get_feedback_responses(cursor)
            logging.debug(f"Fetched feedback responses: {feedback_responses}")
            return {'status': 'success', 'feedback_responses': feedback_responses}
        except Exception as e:
            logging.error(f"Error in view_feedback_responses: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve feedback responses'}