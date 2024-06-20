import socket
import threading
import json
from datetime import datetime
from decimal import Decimal
from database import get_db_connection  # Ensure database.py is available
import logging

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.db = get_db_connection()
        self.start_server()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.clients.append(client_socket)

    def handle_client(self, client_socket):
        while True:
            try:
                request = client_socket.recv(1024).decode()
                if not request:
                    break
                print(f"Received request: {request}")
                response = self.handle_request(json.loads(request))
                response_json = json.dumps(response, cls=CustomJSONEncoder)
                print(f"Sending response: {response_json}")
                client_socket.sendall(response_json.encode())
            except json.JSONDecodeError as json_err:
                logging.error(f"JSON decode error: {json_err}")
                error_response = json.dumps({'status': 'error', 'message': 'Invalid JSON format'})
                client_socket.sendall(error_response.encode())
            except Exception as e:
                logging.error(f"Error: {e}")
                error_response = json.dumps({'status': 'error', 'message': 'Server error'})
                client_socket.sendall(error_response.encode())
                client_socket.close()
                break

    def handle_request(self, request):
        action = request['action']
        if action == 'login':
            return self.login(request['employee_id'], request['password'])
        elif action == 'view_menu':
            return self.view_menu()
        elif action == 'add_menu_item':
            return self.add_menu_item(request['name'], request['price'], request['availability'], request['role'])
        elif action == 'update_menu_item':
            return self.update_menu_item(request['item_id'], request['name'], request['price'], request['availability'])
        elif action == 'delete_menu_item':
            return self.delete_menu_item(request['item_id'])
        elif action == 'get_recommendations':
            return self.get_recommendations()
        elif action == 'send_notification':
            return self.send_notification(request['message'], request['role'])
        elif action == 'rate_menu_item':
            return self.rate_menu_item(request['user_id'], request['menu_item_id'], request['rating'], request['review'])
        elif action == 'send_report':
            return self.send_report(request['report'])
        else:
            return {'status': 'error', 'message': 'Invalid action'}

    def login(self, employee_id, password):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE employee_id=%s AND password=%s", (employee_id, password))
            user = cursor.fetchone()
            if user:
                return {'status': 'success', 'role': user['role']}
            else:
                return {'status': 'error', 'message': 'Invalid credentials'}
        except Exception as e:
            logging.error(f"Error in login: {e}")
            return {'status': 'error', 'message': 'Failed to login'}

    def view_menu(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu_items")
            menu = cursor.fetchall()

            # Convert Decimal and datetime to string in the menu items
            for item in menu:
                for key, value in item.items():
                    if isinstance(value, Decimal):
                        item[key] = str(value)
                    elif isinstance(value, datetime):
                        item[key] = value.isoformat()

            return {'status': 'success', 'menu': menu}
        except Exception as e:
            logging.error(f"Error in view_menu: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve menu'}

    def add_menu_item(self, name, price, availability, role):
        try:
            logging.debug(f"Add menu item requested by role: {role}")
            if role != 1:  # Only Admin can add items
                logging.error("Permission denied: only admin can add menu items")
                return {'status': 'error', 'message': 'Permission denied'}
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO menu_items (name, price, availability) VALUES (%s, %s, %s)",
                (name, price, availability)
            )
            self.db.commit()
            return {'status': 'success', 'message': 'Menu item added'}
        except Exception as e:
            logging.error(f"Error in add_menu_item: {e}")  # Detailed logging
            return {'status': 'error', 'message': 'Failed to add menu item'}

    def update_menu_item(self, item_id, name, price, availability):
        try:
            cursor = self.db.cursor()
            query = "UPDATE menu_items SET"
            params = []
            if name:
                query += " name=%s,"
                params.append(name)
            if price:
                query += " price=%s,"
                params.append(price)
            if availability:
                query += " availability=%s,"
                params.append(availability)
            query = query.rstrip(',')
            query += " WHERE id=%s"
            params.append(item_id)

            cursor.execute(query, tuple(params))
            self.db.commit()
            return {'status': 'success', 'message': 'Menu item updated'}
        except Exception as e:
            logging.error(f"Error in update_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to update menu item'}

    def delete_menu_item(self, item_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
            self.db.commit()
            return {'status': 'success', 'message': 'Menu item deleted'}
        except Exception as e:
            logging.error(f"Error in delete_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to delete menu item'}

    def get_recommendations(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT mi.id, mi.name, mi.price, AVG(r.rating) as average_rating
                FROM menu_items mi
                JOIN ratings r ON mi.id = r.menu_item_id
                GROUP BY mi.id, mi.name, mi.price
                ORDER BY average_rating DESC
                LIMIT 5
            """)
            recommendations = cursor.fetchall()

            # Convert Decimal and datetime to string in the recommendations
            for item in recommendations:
                for key, value in item.items():
                    if isinstance(value, Decimal):
                        item[key] = str(value)
                    elif isinstance(value, datetime):
                        item[key] = value.isoformat()

            # Send notification to employees about the recommendations
            self.send_notification_to_all_employees("Chef's Recommendations: " + ', '.join([item['name'] for item in recommendations]))

            return {'status': 'success', 'recommendations': recommendations}
        except Exception as e:
            logging.error(f"Error in get_recommendations: {e}")
            return {'status': 'error', 'message': 'Failed to get recommendations'}

    def send_notification_to_all_employees(self, message):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id FROM users WHERE role = 3")  # Role 3 is Employee
            employees = cursor.fetchall()
            for employee in employees:
                cursor.execute("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", (employee['id'], message))
            self.db.commit()
        except Exception as e:
            logging.error(f"Error in send_notification_to_all_employees: {e}")

    def send_notification(self, message, role):
        if role != 2:  # Only Chef can send notifications
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO notifications (message, user_id) VALUES (%s, %s)", (message, None))  # Broadcast notification
            self.db.commit()
            return {'status': 'success', 'message': 'Notification sent'}
        except Exception as e:
            logging.error(f"Error in send_notification: {e}")
            return {'status': 'error', 'message': 'Failed to send notification'}

    def rate_menu_item(self, user_id, menu_item_id, rating, review):
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO ratings (menu_item_id, rating, review, user_id) VALUES (%s, %s, %s, %s)",
                           (menu_item_id, rating, review, user_id))
            self.db.commit()
            return {'status': 'success', 'message': 'Rating submitted'}
        except Exception as e:
            logging.error(f"Error in rate_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to submit rating'}

    def send_report(self, report):
        # Implement report sending logic here
        return {'status': 'success', 'message': 'Report sent'}

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server_config = {
        'host': 'localhost',
        'port': 12346  # Change this to a different port if 12345 is in use
    }
    Server(server_config['host'], server_config['port'])
