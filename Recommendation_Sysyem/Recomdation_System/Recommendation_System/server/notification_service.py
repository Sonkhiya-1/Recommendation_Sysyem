# import json
# import logging
# from utils.custom_json_encoder import CustomJSONEncoder

# class NotificationService:
#     def __init__(self, db, clients):
#         self.db = db
#         self.clients = clients

    # def view_notifications(self, request, client_socket):
    #     user_id = request['user_id']
    #     try:
    #         cursor = self.db.cursor(dictionary=True)
    #         cursor.execute("SELECT * FROM notifications WHERE user_id=%s AND viewed=FALSE", (user_id,))
    #         notifications = cursor.fetchall()
    #         logging.debug(f"Fetched notifications for user {user_id}: {notifications}")

    #         # Mark notifications as viewed after fetching them
    #         if notifications:
    #             cursor.execute("UPDATE notifications SET viewed=TRUE WHERE user_id=%s AND viewed=FALSE", (user_id,))
    #             self.db.commit()
    #             logging.debug(f"Marked notifications as viewed for user {user_id}")

    #         # Fetch the most recent rollout items
    #         rollout_items = []
    #         if notifications:
    #             cursor.execute("""
    #                 SELECT ri.menu_item_id, mi.name, ri.price, ri.timestamp
    #                 FROM rollout_items ri
    #                 JOIN menu_items mi ON ri.menu_item_id = mi.id
    #                 WHERE ri.chosen = TRUE
    #                 ORDER BY ri.timestamp DESC
    #                 LIMIT 5  -- Limit the number of items returned
    #             """)
    #             rollout_items = cursor.fetchall()
    #             logging.debug(f"Fetched rollout items: {rollout_items}")

    #         return {'status': 'success', 'notifications': notifications, 'rollout_items': rollout_items}
    #     except Exception as e:
    #         logging.error(f"Error in view_notifications: {e}")
    #         return {'status': 'error', 'message': 'Failed to retrieve notifications'}
    
import json
import logging

class NotificationService:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def view_notifications(self, request, client_socket):
        user_id = request['user_id']
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM notifications WHERE user_id=%s AND viewed=FALSE", (user_id,))
            notifications = cursor.fetchall()
            logging.debug(f"Fetched notifications for user {user_id}: {notifications}")

            # Mark notifications as viewed after fetching them
            if notifications:
                cursor.execute("UPDATE notifications SET viewed=TRUE WHERE user_id=%s AND viewed=FALSE", (user_id,))
                self.db.commit()
                logging.debug(f"Marked notifications as viewed for user {user_id}")

            # Fetch only the most recent set of rollout items
            rollout_items = []
            if notifications:
                cursor.execute("""
                    SELECT ri.menu_item_id, mi.name, ri.price, ri.timestamp
                    FROM rollout_items ri
                    JOIN menu_items mi ON ri.menu_item_id = mi.id
                    WHERE ri.timestamp = (
                        SELECT MAX(timestamp)
                        FROM rollout_items
                        WHERE chosen = TRUE
                    )
                """)
                rollout_items = cursor.fetchall()
                logging.debug(f"Fetched rollout items: {rollout_items}")

            return {'status': 'success', 'notifications': notifications, 'rollout_items': rollout_items}
        except Exception as e:
            logging.error(f"Error in view_notifications: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve notifications'}

        
    def send_notification(self, request, client_socket):
        user_id = request['user_id']
        message = request['message']
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO notifications (user_id, message, viewed) VALUES (%s, %s, %s)", (user_id, message, False))
            self.db.commit()
            return {'status': 'success', 'message': 'Notification sent'}
        except Exception as e:
            logging.error(f"Error in send_notification: {e}")
            return {'status': 'error', 'message': 'Failed to send notification'}

    # def _send_notification_to_all_employees(self, message):
    #     try:
    #         cursor = self.db.cursor(dictionary=True)
    #         cursor.execute("SELECT id FROM users WHERE role = 3")
    #         employees = cursor.fetchall()
    #         logging.debug(f"Employees to notify: {employees}")

    #         for employee in employees:
    #             cursor.execute("INSERT INTO notifications (user_id, message, viewed) VALUES (%s, %s, %s)", (employee['id'], message, False))
    #         self.db.commit()
    #         logging.debug("Notifications inserted into the database.")
    #         self._broadcast_notification(message)
    #     except Exception as e:
    #         logging.error(f"Error in send_notification_to_all_employees: {e}")

    # def _broadcast_notification(self, message):
    #     for client_socket, role in self.clients.items():
    #         if role == 3:
    #             try:
    #                 notification = json.dumps({'status': 'notification', 'message': message}, cls=CustomJSONEncoder)
    #                 client_socket.sendall(notification.encode())
    #                 logging.debug(f"Notification sent to client: {client_socket}")
    #             except Exception as e:
    #                 logging.error(f"Error sending notification to client: {e}")
