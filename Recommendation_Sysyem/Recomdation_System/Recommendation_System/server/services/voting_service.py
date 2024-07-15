import logging
import datetime
from queries.voting_queries import insert_vote, get_vote_counts

class VotingService:
    def __init__(self, db):
        self.db = db

    def vote_for_menu_item(self, request, client_socket):
        try:
            user_id, menu_item_id, meal_type = request['user_id'], request['dish_id'], request['meal_type']
            cursor = self.db.cursor()
            insert_vote(cursor, menu_item_id, user_id, meal_type)
            self.db.commit()
            return {'status': 'success', 'message': 'Vote submitted'}
        except Exception as e:
            logging.error(f"Error in vote_for_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to submit vote'}

    def view_vote_counts(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            today = datetime.date.today()
            vote_counts = get_vote_counts(cursor, today)
            logging.debug(f"Vote counts fetched: {vote_counts}")

            return {'status': 'success', 'vote_counts': vote_counts}
        except Exception as e:
            logging.error(f"Error in view_vote_counts: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve vote counts'}
