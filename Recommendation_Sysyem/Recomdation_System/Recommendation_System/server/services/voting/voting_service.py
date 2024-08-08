import logging
import datetime
from server.services.voting.voting_queries import insert_vote, get_vote_counts

class VotingService:
    def __init__(self, db):
        self.db = db

    def vote_for_menu_item(self, request, client_socket):
        try:
            user_id = request['user_id']
            dish_ids = request['dish_ids'] 
            meal_type = request['meal_type']
            cursor = self.db.cursor()

            for dish_id in dish_ids:
                insert_vote(cursor, dish_id, user_id, meal_type)

            self.db.commit()
            return {'status': 'success', 'message': 'Vote submitted'}
        except Exception as e:
            logging.error(f"Error in vote_for_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to submit vote'}

    def view_vote_counts(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            today = datetime.date.today()
            query = """
                SELECT mi.name, v.meal_type, COUNT(v.id) as vote_count
                FROM votes v
                JOIN menu_items mi ON v.menu_item_id = mi.id
                JOIN rollout_items ri ON ri.menu_item_id = mi.id
                WHERE DATE(v.voted_at) = %s AND ri.chosen = TRUE
                GROUP BY mi.name, v.meal_type
            """
            logging.debug(f"Executing query: {query} with date {today}")

            cursor.execute(query, (today,))
            vote_counts = cursor.fetchall()
            logging.debug(f"Vote counts fetched: {vote_counts}")

            return {'status': 'success', 'vote_counts': vote_counts}
        except Exception as e:
            logging.error(f"Error in view_vote_counts: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve vote counts'}