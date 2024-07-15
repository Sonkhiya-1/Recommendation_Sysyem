import socket
import threading
import logging
import json
from utils.custom_json_encoder import CustomJSONEncoder
from utils.db_connection import get_db_connection
from server.services.feedback.feedback_service import FeedbackService
from server.services.menu.menu_service import MenuService
from server.services.notifications.notification_service import NotificationService
from server.services.recommendation.recommendation_service import RecommendationService
from server.services.voting.voting_service import VotingService
from server.services.dicard_item.discard_item_service import DiscardItemService
from server.services.user_management.user_management import UserManagement
from server.request_handler import RequestHandler

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.db = get_db_connection()
        self.request_handler = self.create_request_handler()
        self.start_server()

    def create_request_handler(self):
        notification_service = NotificationService(self.db, self.clients)
        user_management = UserManagement(self.db, self.clients)
        menu_service = MenuService(self.db, notification_service)
        voting_service = VotingService(self.db)
        feedback_service = FeedbackService(self.db)
        recommendation_service = RecommendationService(self.db, self.clients)
        discard_item_service = DiscardItemService(self.db, notification_service)

        return RequestHandler({
            'notification_service': notification_service,
            'user_management': user_management,
            'menu_service': menu_service,
            'voting_service': voting_service,
            'feedback_service': feedback_service,
            'recommendation_service': recommendation_service,
            'discard_item_service': discard_item_service
        })

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        logging.info(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                request = client_socket.recv(1024).decode()
                if not request:
                    break
                logging.debug(f"Received request: {request}")
                response = self.request_handler.handle_request(json.loads(request), client_socket)
                response_json = json.dumps(response, cls=CustomJSONEncoder)
                logging.debug(f"Sending response: {response_json}")
                client_socket.sendall(response_json.encode())
            except json.JSONDecodeError as json_err:
                logging.error(f"JSON decode error: {json_err}")
                self._send_error_response(client_socket, 'Invalid JSON format')
            except Exception as e:
                logging.error(f"Error: {e}")
                self._send_error_response(client_socket, 'Server error')
                client_socket.close()
                break

    def _send_error_response(self, client_socket, message):
        error_response = json.dumps({'status': 'error', 'message': message})
        client_socket.sendall(error_response.encode())


