# import logging
# import json
# from datetime import datetime
# from utils.custom_json_encoder import CustomJSONEncoder

# class RecommendationService:
#     def __init__(self, db, clients):
#         self.db = db
#         self.clients = clients

#     def get_recommendations(self, request, client_socket):
#         if request.get('role') != 2:
#             return {'status': 'error', 'message': 'Permission denied'}
#         try:
#             cursor = self.db.cursor(dictionary=True)
#             query = """
#                 SELECT mi.id, mi.name, mi.price, mi.average_rating, 
#                        (SELECT COUNT(*) FROM feedback f WHERE f.menu_item_id = mi.id AND f.sentiment = 'positive') as positive_feedback,
#                        (SELECT COUNT(*) FROM feedback f WHERE f.menu_item_id = mi.id AND f.sentiment = 'negative') as negative_feedback
#                 FROM menu_items mi
#                 ORDER BY mi.average_rating DESC, positive_feedback DESC, negative_feedback ASC
#                 LIMIT 5
#             """
#             logging.debug(f"Executing query: {query}")
#             cursor.execute(query)
#             recommendations = cursor.fetchall()
#             logging.debug(f"Recommendations fetched: {recommendations}")
#             recommendations_json = json.dumps(recommendations, cls=CustomJSONEncoder)
#             return {'status': 'success', 'recommendations': json.loads(recommendations_json)}
#         except Exception as e:
#             logging.error(f"Error in get_recommendations: {e}")
#             return {'status': 'error', 'message': 'Failed to get recommendations'}

#     def choose_recommendations(self, request, client_socket):
#         if request.get('role') != 2:
#             return {'status': 'error', 'message': 'Permission denied'}
#         try:
#             menu_item_ids = request['menu_item_ids']
#             user_id = request['user_id']
#             current_timestamp = datetime.now()
#             cursor = self.db.cursor(dictionary=True)
#             for menu_item_id in menu_item_ids:
#                 cursor.execute("SELECT price FROM menu_items WHERE id=%s", (menu_item_id,))
#                 result = cursor.fetchone()
#                 if result:
#                     price = result['price']
#                     logging.debug(f"Fetched price for menu_item_id {menu_item_id}: {price}")
#                     cursor.execute("INSERT INTO rollout_items (menu_item_id, chef_id, chosen, price, timestamp) VALUES (%s, %s, %s, %s, %s)", (menu_item_id, user_id, True, price, current_timestamp))
#                     self.db.commit()
#                     logging.debug(f"Inserted rollout item: {menu_item_id} by user: {user_id} with price: {price} at {current_timestamp}")

#             self._send_notification_to_all_employees(f"New rollout items available. Please vote for your preferred items.")
#             return {'status': 'success', 'message': 'Recommendations chosen'}
#         except Exception as e:
#             logging.error(f"Error in choose_recommendations: {e}")
#             return {'status': 'error', 'message': 'Failed to choose recommendations'}

#     def _send_notification_to_all_employees(self, message):
#         try:
#             cursor = self.db.cursor(dictionary=True)
#             cursor.execute("SELECT id FROM users WHERE role = 3")
#             employees = cursor.fetchall()
#             for employee in employees:
#                 logging.debug(f"Inserting notification for employee {employee['id']}")
#                 cursor.execute("INSERT INTO notifications (user_id, message, viewed) VALUES (%s, %s, %s)", (employee['id'], message, False))
#             self.db.commit()
#             self._broadcast_notification(message)
#         except Exception as e:
#             logging.error(f"Error in send_notification_to_all_employees: {e}")

#     def _broadcast_notification(self, message):
#         for client_socket, role in self.clients.items():
#             if role == 3:
#                 try:
#                     notification = json.dumps({'status': 'notification', 'message': message}, cls=CustomJSONEncoder)
#                     client_socket.sendall(notification.encode())
#                 except Exception as e:
#                     logging.error(f"Error sending notification to client: {e}")


import logging
import json
from datetime import datetime
from utils.custom_json_encoder import CustomJSONEncoder

class RecommendationService:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def get_recommendations(self, request, client_socket):
        if request.get('role') != 2:  # Only allow chefs to get recommendations
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            user_id = request['user_id']

            # Fetch user preferences
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
            user_preferences = cursor.fetchone()

            # Fetch recommendations
            cursor.execute("""
                SELECT mi.id, mi.name, mi.price, mi.average_rating, mi.dietary_category, mi.spice_level, mi.is_sweet
                FROM menu_items mi
                ORDER BY mi.average_rating DESC
                LIMIT 10  -- Fetch more items to have room for sorting
            """)
            recommendations = cursor.fetchall()

            if user_preferences:
                # Filter and sort based on preferences
                recommendations = self._filter_and_sort_recommendations(recommendations, user_preferences)

            recommendations_json = json.dumps(recommendations, cls=CustomJSONEncoder)
            return {'status': 'success', 'recommendations': json.loads(recommendations_json)}
        except Exception as e:
            logging.error(f"Error in get_recommendations: {e}")
            return {'status': 'error', 'message': 'Failed to get recommendations'}

    def _filter_and_sort_recommendations(self, recommendations, preferences):
        dietary_order = {
            'Vegetarian': 1,
            'Eggetarian': 2,
            'Non Vegetarian': 3
        }
        
        # Filter based on dietary preference
        filtered_recommendations = [
            item for item in recommendations 
            if self._matches_dietary_preference(item, preferences['dietary_preference'])
        ]

        # Sort based on multiple preferences
        filtered_recommendations.sort(key=lambda item: (
            dietary_order.get(item['dietary_category'], 4),
            self._spice_level_score(item['spice_level'], preferences['spice_level']),
            not item['is_sweet'] if preferences['sweet_tooth'] else item['is_sweet'],  # Prefer sweet items if user has sweet tooth
            -item['average_rating'],  # Higher ratings first
            item['price']  # Assuming lower price is preferred
        ))
        
        return filtered_recommendations

    def _matches_dietary_preference(self, item, preference):
        if preference == 'Vegetarian' and item['dietary_category'] == 'Vegetarian':
            return True
        if preference == 'Eggetarian' and item['dietary_category'] in ['Vegetarian', 'Eggetarian']:
            return True
        if preference == 'Non Vegetarian':
            return True  # All items are fine for non-vegetarians
        return False

    def _spice_level_score(self, item_spice, preferred_spice):
        spice_levels = {'Low': 1, 'Medium': 2, 'High': 3}
        return abs(spice_levels.get(item_spice, 2) - spice_levels.get(preferred_spice, 2))

    def choose_recommendations(self, request, client_socket):
        if request.get('role') != 2:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            menu_item_ids = request['menu_item_ids']
            user_id = request['user_id']
            current_timestamp = datetime.now()
            cursor = self.db.cursor(dictionary=True)
            for menu_item_id in menu_item_ids:
                cursor.execute("SELECT price FROM menu_items WHERE id=%s", (menu_item_id,))
                result = cursor.fetchone()
                if result:
                    price = result['price']
                    logging.debug(f"Fetched price for menu_item_id {menu_item_id}: {price}")
                    cursor.execute("INSERT INTO rollout_items (menu_item_id, chef_id, chosen, price, timestamp) VALUES (%s, %s, %s, %s, %s)", (menu_item_id, user_id, True, price, current_timestamp))
                    self.db.commit()
                    logging.debug(f"Inserted rollout item: {menu_item_id} by user: {user_id} with price: {price} at {current_timestamp}")

            self._send_notification_to_all_employees(f"New rollout items available. Please vote for your preferred items.")
            return {'status': 'success', 'message': 'Recommendations chosen'}
        except Exception as e:
            logging.error(f"Error in choose_recommendations: {e}")
            return {'status': 'error', 'message': 'Failed to choose recommendations'}

    def _send_notification_to_all_employees(self, message):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE role = 3")
            employees = cursor.fetchall()
            for employee in employees:
                logging.debug(f"Inserting notification for employee {employee['id']}")
                cursor.execute("INSERT INTO notifications (user_id, message, viewed) VALUES (%s, %s, %s)", (employee['id'], message, False))
            self.db.commit()
            self._broadcast_notification(message)
        except Exception as e:
            logging.error(f"Error in send_notification_to_all_employees: {e}")

    def _broadcast_notification(self, message):
        for client_socket, role in self.clients.items():
            if role == 3:
                try:
                    notification = json.dumps({'status': 'notification', 'message': message}, cls=CustomJSONEncoder)
                    client_socket.sendall(notification.encode())
                except Exception as e:
                    logging.error(f"Error sending notification to client: {e}")
