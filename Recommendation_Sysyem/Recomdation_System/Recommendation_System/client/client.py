from responses.notification_handler import NotificationHandler
import socket
import json
import threading
import logging
from menu_display import MenuDisplay
from request_data import RequestData
from notification_listener import NotificationListener
from utils.socket_utils import create_socket
from responses.menu_handler import MenuHandler
from responses.base_response_handler import BaseResponseHandler
from responses.discard_list_handler import DiscardListHandler
from responses.message_handler import MessageHandler
from responses.recommendations_handler import RecommendationsHandler
from responses.vote_counts_handler import VoteCountsHandler

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

    def send_request(self, request):
        try:
            self.socket.sendall(json.dumps(request).encode())
            response = self.socket.recv(4096).decode()
            return json.loads(response)
        except socket.timeout:
            logging.error("Socket timeout occurred")
            return {'status': 'error', 'message': 'Socket timeout'}
        except Exception as e:
            logging.error(f"Error sending request: {e}")
            return {'status': 'error', 'message': str(e)}

    def login(self):
        employee_id = input("Enter Employee ID: ")
        password = input("Enter Password: ")
        request = {"action": "login", "employee_id": employee_id, "password": password}
        response = self.send_request(request)
        if response['status'] == 'success':
            self.role = response.get('role')
            self.user_id = response.get('user_id')
            return True
        else:
            print(f"Login failed: {response['message']}")
            return False

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
                    print("Invalid action selected. Please try again.")
                    continue
                response = self.send_request(request)
                self.handle_response(response, action)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def _is_logout_action(self, action):
        return (
            (self.role == 1 and action == 8) or
            (self.role == 2 and action == 10) or
            (self.role == 3 and action == 6)
        )

    def handle_response(self, response, action):
        if response['status'] == 'success':
            if action == 1:
                MenuHandler.display_menu(response)
            elif action == 2:
                if self.role == 2:  
                    RecommendationsHandler.display_recommendations(response)
                elif self.role == 3:  
                    VoteCountsHandler.display_vote_counts(response)
            elif action == 3 and self.role == 2: 
                RecommendationsHandler.display_recommendations(response)
            elif action == 4:
                if self.role == 2:
                    VoteCountsHandler.display_vote_counts(response)
                elif self.role == 3:
                    NotificationHandler.display_notifications(response)
                    
            elif action == 5 and self.role == 2:  
                MessageHandler.display_message(response)
            elif action == 6 and self.role == 2: 
                MessageHandler.display_message(response)
            elif action == 7:
                DiscardListHandler.display_discard_list(response)
            elif action == 8:
                MessageHandler.display_message(response)
            elif action == 9:
                MessageHandler.display_message(response)
            elif action == 10:
                print("Logging out...")
            else:
                print("Action completed successfully.")
        else:
            print(f"Error: {response['message']}")


if __name__ == "__main__":
    client = Client('localhost', 12346)
    if client.login():
        client.main_loop()
    else:
        print("Exiting the program due to failed login.")
