import logging
from sentiment_analysis import SentimentAnalysis

class FeedbackService:
    def __init__(self, db):
        self.db = db
from sentiment_analysis import SentimentAnalysis

class FeedbackService:
    def __init__(self, db):
        self.db = db

    def submit_feedback(self, request, client_socket):
        try:
            user_id, comment, item_id = request['user_id'], request['comment'], request['item_id']
            sentiment = SentimentAnalysis.analyze(comment)
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO feedback (user_id, comment, sentiment, menu_item_id) VALUES (%s, %s, %s, %s)", (user_id, comment, sentiment, item_id))
            self.db.commit()
            self.update_average_rating(item_id)
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            logging.error(f"Error in submit_feedback: {e}")
            return {'status': 'error', 'message': 'Failed to submit feedback'}

    def send_feedback(self, request, client_socket):
        try:
            user_id, comment, item_id = request['user_id'], request['comment'], request['item_id']
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO feedback (user_id, comment, menu_item_id) VALUES (%s, %s, %s)", (user_id, comment, item_id))
            self.db.commit()
            self.update_average_rating(item_id)
            return {'status': 'success', 'message': 'Feedback sent'}
        except Exception as e:
            logging.error(f"Error in send_feedback: {e}")
            return {'status': 'error', 'message': 'Failed to send feedback'}

    def update_average_rating(self, item_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT AVG(CASE WHEN sentiment = 'positive' THEN 5 WHEN sentiment = 'neutral' THEN 3 WHEN sentiment = 'negative' THEN 1 END) as average_rating FROM feedback WHERE menu_item_id = %s", (item_id,))
            avg_rating = cursor.fetchone()['average_rating']
            cursor.execute("UPDATE menu_items SET average_rating = %s WHERE id = %s", (avg_rating, item_id))
            self.db.commit()
        except Exception as e:
            logging.error(f"Error in update_average_rating: {e}")


    def submit_feedback(self, request, client_socket):
        try:
            user_id, comment, item_id = request['user_id'], request['comment'], request['item_id']
            sentiment = SentimentAnalysis.analyze(comment)
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO feedback (user_id, comment, sentiment, menu_item_id) VALUES (%s, %s, %s, %s)", (user_id, comment, sentiment, item_id))
            self.db.commit()
            self.update_average_rating(item_id)
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            logging.error(f"Error in submit_feedback: {e}")
            return {'status': 'error', 'message': 'Failed to submit feedback'}

    def send_feedback(self, request, client_socket):
        try:
            user_id, comment, item_id = request['user_id'], request['comment'], request['item_id']
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO feedback (user_id, comment, menu_item_id) VALUES (%s, %s, %s)", (user_id, comment, item_id))
            self.db.commit()
            self.update_average_rating(item_id)
            return {'status': 'success', 'message': 'Feedback sent'}
        except Exception as e:
            logging.error(f"Error in send_feedback: {e}")
            return {'status': 'error', 'message': 'Failed to send feedback'}

    def update_average_rating(self, item_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT AVG(CASE WHEN sentiment = 'positive' THEN 5 WHEN sentiment = 'neutral' THEN 3 WHEN sentiment = 'negative' THEN 1 END) as average_rating FROM feedback WHERE menu_item_id = %s", (item_id,))
            avg_rating = cursor.fetchone()['average_rating']
            cursor.execute("UPDATE menu_items SET average_rating = %s WHERE id = %s", (avg_rating, item_id))
            self.db.commit()
        except Exception as e:
            logging.error(f"Error in update_average_rating: {e}")
