import logging
import json
from datetime import datetime
from queries.recommendation_queries import get_user_preferences, get_recommendations, get_menu_item_price, insert_rollout_item
from utils.custom_json_encoder import CustomJSONEncoder
from queries.notification_queries import get_employee_ids, insert_notification

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

            logging.debug(f"Fetching preferences for user_id={user_id}")

            cursor = self.db.cursor(dictionary=True)
            user_preferences = get_user_preferences(cursor, user_id)
            logging.debug(f"User preferences: {user_preferences}")

            recommendations = get_recommendations(cursor)
            logging.debug(f"Fetched recommendations: {recommendations}")

            if user_preferences:
                recommendations = self._filter_and_sort_recommendations(recommendations, user_preferences)
                logging.debug(f"Filtered and sorted recommendations: {recommendations}")

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
        
        filtered_recommendations = [
            item for item in recommendations 
            if self._matches_dietary_preference(item, preferences['dietary_preference'])
        ]

        filtered_recommendations.sort(key=lambda item: (
            dietary_order.get(item['dietary_category'], 4),
            self._spice_level_score(item['spice_level'], preferences['spice_level']),
            not item['is_sweet'] if preferences['sweet_tooth'] else item['is_sweet'],
            -item['average_rating'],
            item['price']
        ))

        return filtered_recommendations

    def _matches_dietary_preference(self, item, preference):
        if preference == 'Vegetarian' and item['dietary_category'] == 'Vegetarian':
            return True
        if preference == 'Eggetarian' and item['dietary_category'] in ['Vegetarian', 'Eggetarian']:
            return True
        if preference == 'Non Vegetarian':
            return True
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
                result = get_menu_item_price(cursor, menu_item_id)
                if result:
                    price = result['price']
                    logging.debug(f"Fetched price for menu_item_id {menu_item_id}: {price}")
                    insert_rollout_item(cursor, menu_item_id, user_id, price, current_timestamp)
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