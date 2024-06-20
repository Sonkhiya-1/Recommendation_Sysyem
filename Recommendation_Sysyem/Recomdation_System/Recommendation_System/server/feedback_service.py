import logging

class FeedbackService:
    def __init__(self, db):
        self.db = db

    def submit_feedback(self, request, client_socket):
        try:
            user_id, comment = request['user_id'], request['comment']
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO feedback (user_id, comment) VALUES (%s, %s)", (user_id, comment))
            self.db.commit()
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            logging.error(f"Error in submit_feedback: {e}")
            return {'status': 'error', 'message': 'Failed to submit feedback'}

    def view_reports(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM reports")
            reports = cursor.fetchall()
            return {'status': 'success', 'reports': reports}
        except Exception as e:
            logging.error(f"Error in view_reports: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve reports'}



