
from datetime import datetime, timedelta
from client.menu_display import MenuDisplay
from client.request_data import RequestData
import socket
import json
import threading
import logging
from datetime import datetime, timedelta
from client.notification_listener import NotificationListener
from client.utils.socket_utils import create_socket
from client.handlers.action_handler import initialize_action_handlers
from client.handlers.login_handler import LoginHandler

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = create_socket(self.host, self.port)
        self.role = None
        self.user_id = None
        self.menu_display = MenuDisplay(self)
        self.request_data = RequestData(self)
        self.notification_listener = NotificationListener(self.socket)
        self.notification_thread = threading.Thread(
            target=self.notification_listener.listen_for_notifications, daemon=True)
        self.notification_thread.start()
        self.action_handlers = initialize_action_handlers(self)
        self.login_handler = LoginHandler(self)

    def send_request(self, request):
        try:
            self.socket.sendall(json.dumps(request).encode())

            buffer = ""
            while True:
                data = self.socket.recv(4096).decode()
                if not data:
                    break
                buffer += data

                try:
                    response = json.loads(buffer)
                    buffer = ""
                    return response
                except json.JSONDecodeError as e:
                    logging.debug(f"Incomplete JSON data received, continuing to read. Error: {e}")

        except socket.timeout:
            logging.error("Socket timeout occurred")
            return {'status': 'error', 'message': 'Socket timeout'}
        except Exception as e:
            logging.error(f"Error sending request: {e}")
            return {'status': 'error', 'message': str(e)}

    def main_loop(self):
        while True:
            self.menu_display.display_menu(self.role)
            try:
                action = int(input("Enter your choice: "))
                if self._is_logout_action(action):
                    print("Logging out...")
                    break
                request = self.request_data.get_request_data(action, self.role, self.user_id)
                if not request:
                    continue
                
                response = self.send_request(request)
                self.handle_response(response, action)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def _is_logout_action(self, action):
        return (
            (self.role == 1 and action == 8) or  # Admin logout action
            (self.role == 2 and action == 11) or  # Chef logout action
            (self.role == 3 and action == 8)  # Employee logout action
        )

    def handle_response(self, response, action):
        if response['status'] == 'success':
            handler = self.action_handlers.get(action)
            if isinstance(handler, dict):
                handler = handler.get(self.role)
            if handler:
                handler(response)
            else:
                print("Action completed successfully.")
        else:
            print(f"Error: {response['message']}")

    def _logout_handler(self, response):
        print("Logging out...")

    def handle_profile_update_response(self, response):
        if response['status'] == 'success':
            print("Profile updated successfully.")
        else:
            print(f"Failed to update profile: {response['message']}")
