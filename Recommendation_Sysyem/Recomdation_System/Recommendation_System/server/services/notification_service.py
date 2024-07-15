import logging
import json
from queries.notification_queries import get_notifications, mark_notifications_as_viewed, get_rollout_items, insert_notification, get_employee_ids
from utils.custom_json_encoder import CustomJSONEncoder

class NotificationService:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def view_notifications(self, request, client_socket):
        user_id = request['user_id']
        role = request.get('role')
        try:
            cursor = self.db.cursor(dictionary=True)
            notifications = get_notifications(cursor, user_id)
            logging.debug(f"Fetched notifications for user {user_id}: {notifications}")

            if notifications:
                mark_notifications_as_viewed(cursor, user_id)
                self.db.commit()
                logging.debug(f"Marked notifications as viewed for user {user_id}")

            rollout_items = []
            if role == 3 and notifications:
                rollout_items = get_rollout_items(cursor)
                logging.debug(f"Fetched rollout items: {rollout_items}")

                cursor.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
                user_preferences = cursor.fetchone()
                if user_preferences:
                    rollout_items = self.sort_rollout_items(rollout_items, user_preferences)
                else:
                    logging.warning(f"No preferences found for user {user_id}")

            return {'status': 'success', 'notifications': notifications, 'rollout_items': rollout_items}
        except Exception as e:
            logging.error(f"Error in view_notifications: {e}")
            return {'status': 'error', 'message': f'Failed to retrieve notifications: {e}'}

    def sort_rollout_items(self, rollout_items, preferences):
        dietary_order = {
            'Vegetarian': 1,
            'Eggetarian': 2,
            'Non Vegetarian': 3
        }

        sorted_items = sorted(rollout_items, key=lambda item: (
            dietary_order.get(item['dietary_category'], 4),
            self.spice_level_score(item['spice_level'], preferences['spice_level']),
            not item['is_sweet'] if preferences['sweet_tooth'] else item['is_sweet'],
            -item['average_rating'],
            item['price']
        ))

        return sorted_items

    def spice_level_score(self, item_spice, preferred_spice):
        spice_levels = {'Low': 1, 'Medium': 2, 'High': 3}
        return abs(spice_levels.get(item_spice, 2) - spice_levels.get(preferred_spice, 2))

    def send_notification(self, request, client_socket):
        user_id = request['user_id']
        message = request['message']
        try:
            cursor = self.db.cursor()
            insert_notification(cursor, user_id, message)
            self.db.commit()
            return {'status': 'success', 'message': 'Notification sent'}
        except Exception as e:
            logging.error(f"Error in send_notification: {e}")
            return {'status': 'error', 'message': 'Failed to send notification'}

    def send_notification_to_all_employees(self, message):
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
                    notification = json.dumps({'status': 'notification', 'message': message})
                    client_socket.sendall(notification.encode())
                except Exception as e:
                    logging.error(f"Error sending notification to client: {e}")
