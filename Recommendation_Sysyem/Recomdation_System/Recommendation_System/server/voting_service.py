

import logging

class VotingService:
    def __init__(self, db):
        self.db = db

    def vote_for_menu_item(self, request, client_socket):
        try:
            user_id, menu_item_id, meal_type = request['user_id'], request['dish_id'], request['meal_type']
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO votes (menu_item_id, user_id, meal_type) VALUES (%s, %s, %s)", (menu_item_id, user_id, meal_type))
            self.db.commit()
            return {'status': 'success', 'message': 'Vote submitted'}
        except Exception as e:
            logging.error(f"Error in vote_for_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to submit vote'}


    def view_vote_counts(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT mi.name, v.meal_type, COUNT(v.id) as vote_count
                FROM votes v
                JOIN menu_items mi ON v.menu_item_id = mi.id
                GROUP BY mi.name, v.meal_type
            """)
            vote_counts = cursor.fetchall()
            return {'status': 'success', 'vote_counts': vote_counts}
        except Exception as e:
            logging.error(f"Error in view_vote_counts: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve vote counts'}



