import logging
import json
from datetime import datetime
from utils.custom_json_encoder import CustomJSONEncoder

class RecommendationService:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def get_recommendations(self, request, client_socket):
        if request.get('role') != 2:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT mi.id, mi.name, mi.price, mi.average_rating, 
                       (SELECT COUNT(*) FROM feedback f WHERE f.menu_item_id = mi.id AND f.sentiment = 'positive') as positive_feedback,
                       (SELECT COUNT(*) FROM feedback f WHERE f.menu_item_id = mi.id AND f.sentiment = 'negative') as negative_feedback
                FROM menu_items mi
                ORDER BY mi.average_rating DESC, positive_feedback DESC, negative_feedback ASC
                LIMIT 5
            """
            logging.debug(f"Executing query: {query}")
            cursor.execute(query)
            recommendations = cursor.fetchall()
            logging.debug(f"Recommendations fetched: {recommendations}")
            recommendations_json = json.dumps(recommendations, cls=CustomJSONEncoder)
            return {'status': 'success', 'recommendations': json.loads(recommendations_json)}
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
