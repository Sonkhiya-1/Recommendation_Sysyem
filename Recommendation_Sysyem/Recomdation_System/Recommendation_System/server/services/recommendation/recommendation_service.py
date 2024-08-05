# import logging
# import json
# from datetime import datetime
# from server.services.recommendation.recommendation_queries import get_user_preferences, get_recommendations, get_menu_item_price, insert_rollout_item
# from server.services.recommendation.recommendation_utils import filter_and_sort_recommendations
# from server.services.notifications.notification_queries import get_employee_ids, insert_notification
# from utils.custom_json_encoder import CustomJSONEncoder

# class RecommendationService:
#     def __init__(self, db, clients):
#         self.db = db
#         self.clients = clients

#     def get_recommendations(self, request, client_socket):
#         if request.get('role') != 2:  # Only allow chefs to get recommendations
#             return {'status': 'error', 'message': 'Permission denied'}
#         try:
#             user_id = request.get('user_id')
#             if not user_id:
#                 raise ValueError("Missing 'user_id' in request")

#             min_items = request.get('min_items', 3)
#             cursor = self.db.cursor(dictionary=True)
#             user_preferences = get_user_preferences(cursor, user_id)

#             recommendations = get_recommendations(cursor)

#             if user_preferences:
#                 recommendations = filter_and_sort_recommendations(recommendations, user_preferences, min_items)

#             recommendations_json = json.dumps(recommendations, cls=CustomJSONEncoder)
#             return {'status': 'success', 'recommendations': json.loads(recommendations_json), 'min_items': min_items}
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

#             if not menu_item_ids:
#                 self._send_notification_to_all_employees("No recommendations available at this time.")
#                 return {'status': 'success', 'message': 'No recommendations to display'}

#             for menu_item_id in menu_item_ids:
#                 result = get_menu_item_price(cursor, menu_item_id)
#                 if result:
#                     price = result['price']
#                     meal_type = request.get('meal_type')
#                     logging.debug(f"Fetched price for menu_item_id {menu_item_id}: {price}")
#                     insert_rollout_item(cursor, menu_item_id, user_id, price, current_timestamp, meal_type)
#                     self.db.commit()
#                     logging.debug(f"Inserted rollout item: {menu_item_id} by user: {user_id} with price: {price} at {current_timestamp}")

#             self._send_notification_to_all_employees("New rollout items available. Please vote for your preferred items.")
#             return {'status': 'success', 'message': 'Recommendations chosen'}
#         except Exception as e:
#             logging.error(f"Error in choose_recommendations: {e}")
#             return {'status': 'error', 'message': 'Failed to choose recommendations'}

#     def _send_notification_to_all_employees(self, message):
#         try:
#             cursor = self.db.cursor(dictionary=True)
#             employees = get_employee_ids(cursor)
#             for employee in employees:
#                 logging.debug(f"Inserting notification for employee {employee['id']}")
#                 insert_notification(cursor, employee['id'], message)
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
from server.services.recommendation.recommendation_queries import get_user_preferences, get_recommendations, get_menu_item_price_and_meal_type, insert_rollout_item
from server.services.recommendation.recommendation_utils import filter_and_sort_recommendations
from server.services.notifications.notification_queries import get_employee_ids, insert_notification
from utils.custom_json_encoder import CustomJSONEncoder

class RecommendationService:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def get_recommendations(self, request, client_socket):
        if request.get('role') != 2:  # Only allow chefs to get recommendations
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            user_id = request.get('user_id')
            if not user_id:
                raise ValueError("Missing 'user_id' in request")

            min_items = request.get('min_items', 3)
            cursor = self.db.cursor(dictionary=True)
            user_preferences = get_user_preferences(cursor, user_id)

            recommendations = get_recommendations(cursor)

            if user_preferences:
                recommendations = filter_and_sort_recommendations(recommendations, user_preferences, min_items)

            recommendations_json = json.dumps(recommendations, cls=CustomJSONEncoder)
            return {'status': 'success', 'recommendations': json.loads(recommendations_json), 'min_items': min_items}
        except Exception as e:
            logging.error(f"Error in get_recommendations: {e}")
            return {'status': 'error', 'message': 'Failed to get recommendations'}

    def choose_recommendations(self, request, client_socket):
        if request.get('role') != 2:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            menu_item_ids = request['menu_item_ids']
            user_id = request['user_id']
            current_timestamp = datetime.now()
            cursor = self.db.cursor(dictionary=True)

            if not menu_item_ids:
                self._send_notification_to_all_employees("No recommendations available at this time.")
                return {'status': 'success', 'message': 'No recommendations to display'}

            for menu_item_id in menu_item_ids:
                result = get_menu_item_price_and_meal_type(cursor, menu_item_id)  # Fetch both price and meal_type
                if result:
                    price = result['price']
                    meal_type = result['meal_type']  # Fetch the meal_type from the menu_items table
                    logging.debug(f"Fetched price for menu_item_id {menu_item_id}: {price}, meal_type: {meal_type}")
                    insert_rollout_item(cursor, menu_item_id, user_id, price, current_timestamp, meal_type)
                    self.db.commit()
                    logging.debug(f"Inserted rollout item: {menu_item_id} by user: {user_id} with price: {price} at {current_timestamp}")

            self._send_notification_to_all_employees("New rollout items available. Please vote for your preferred items.")
            return {'status': 'success', 'message': 'Recommendations chosen'}
        except Exception as e:
            logging.error(f"Error in choose_recommendations: {e}")
            return {'status': 'error', 'message': 'Failed to choose recommendations'}

    def _send_notification_to_all_employees(self, message):
        try:
            cursor = self.db.cursor(dictionary=True)
            employees = get_employee_ids(cursor)
            for employee in employees:
                logging.debug(f"Inserting notification for employee {employee['id']}")
                insert_notification(cursor, employee['id'], message)
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
