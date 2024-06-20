import socket
import threading
import json
import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="recommendation_system",
        password="Happy@123",
        database="recommendation_system"
    )

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.db = get_db_connection()
        self.start_server()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                response_json = json.dumps(response)
                print(f"Sending response: {response_json}")
                client_socket.sendall(response_json.encode())
            except json.JSONDecodeError as json_err:
                print(f"JSON decode error: {json_err}")
                error_response = json.dumps({'status': 'error', 'message': 'Invalid JSON format'})
                client_socket.sendall(error_response.encode())
            except Exception as e:
                print(f"Error: {e}")
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
        elif action == 'get_recommendations':
            return self.get_recommendations(request['role'])
        elif action == 'send_notification':
            return self.send_notification(request['user_id'], request['message'], request['role'])
        elif action == 'rate_menu_item':
            return self.rate_menu_item(request['user_id'], request['menu_item_id'], request['rating'], request['comment'], request['role'])
        else:
            return {'status': 'error', 'message': 'Invalid action'}

    def login(self, employee_id, password):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE employee_id=%s AND password=%s", (employee_id, password))
        user = cursor.fetchone()
        if user:
            return {'status': 'success', 'role': user['role_id']}
        else:
            return {'status': 'error', 'message': 'Invalid credentials'}

    def view_menu(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu_items")
            menu = cursor.fetchall()
            return {'status': 'success', 'menu': menu}
        except Exception as e:
            print(f"Error in view_menu: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve menu'}

    def add_menu_item(self, name, price, availability, role):
        if role != 1:
            return {'status': 'error', 'message': 'Permission denied'}
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO menu_items (name, price, availability) VALUES (%s, %s, %s)", (name, price, availability))
        self.db.commit()
        return {'status': 'success', 'message': 'Menu item added'}

    def get_recommendations(self, role):
        if role != 2:
            return {'status': 'error', 'message': 'Permission denied'}
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recommendations ORDER BY score DESC LIMIT 5")
        recommendations = cursor.fetchall()
        return {'status': 'success', 'recommendations': recommendations}

    def send_notification(self, user_id, message, role):
        if role != 2:
            return {'status': 'error', 'message': 'Permission denied'}
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", (user_id, message))
        self.db.commit()
        return {'status': 'success', 'message': 'Notification sent'}

    def rate_menu_item(self, user_id, menu_item_id, rating, comment, role):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO feedback (user_id, menu_item_id, rating, comment, feedback_date) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, menu_item_id, rating, comment, datetime.now()))
        self.db.commit()
        return {'status': 'success', 'message': 'Feedback submitted'}

if __name__ == "__main__":
    server = Server('localhost', 12345)
