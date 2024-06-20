

import json
import logging

class NotificationService:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def send_notification(self, request, client_socket):
        if request['role'] != 2:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            message = request['message']
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO notifications (message) VALUES (%s)", (message,))
            self.db.commit()
            self._broadcast_notification(message)
            return {'status': 'success', 'message': 'Notification sent'}
        except Exception as e:
            logging.error(f"Error in send_notification: {e}")
            return {'status': 'error', 'message': 'Failed to send notification'}

    def _broadcast_notification(self, message):
        for client_socket, role in self.clients.items():
            if role == 3:
                try:
                    notification = json.dumps({'status': 'notification', 'message': message})
                    client_socket.sendall(notification.encode())
                except Exception as e:
                    logging.error(f"Error sending notification to client: {e}")

    def view_notifications(self, request, client_socket):
        user_id = request['user_id']
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM notifications WHERE user_id=%s", (user_id,))
            notifications = cursor.fetchall()
            cursor.execute("DELETE FROM notifications WHERE user_id=%s", (user_id,))
            self.db.commit()
            
            # Fetch rollout items
            cursor.execute("""
                SELECT ri.menu_item_id, mi.name, ri.price
                FROM rollout_items ri
                JOIN menu_items mi ON ri.menu_item_id = mi.id
                WHERE ri.chosen = TRUE
            """)
            rollout_items = cursor.fetchall()
            
            return {'status': 'success', 'notifications': notifications, 'rollout_items': rollout_items}
        except Exception as e:
            logging.error(f"Error in view_notifications: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve notifications'}