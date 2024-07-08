import socket
import threading
import logging
import json
from utils.custom_json_encoder import CustomJSONEncoder
from utils.db_connection import get_db_connection
from server.services.feedback_service import FeedbackService
from server.services.menu_service import MenuService
from server.services.notification_service import NotificationService
from server.services.recommendation_service import RecommendationService
from server.services.voting_service import VotingService
from server.services.discard_item_service import DiscardItemService
from server.user_management import UserManagement
from server.request_handler import RequestHandler


def create_request_handler(db, clients):
    
    notification_service = NotificationService(db, clients)
    user_management = UserManagement(db, clients)
    menu_service = MenuService(db, notification_service)
    voting_service = VotingService(db)
    feedback_service = FeedbackService(db)
    recommendation_service = RecommendationService(db, clients)
    discard_item_service = DiscardItemService(db, notification_service)

    # Return the initialized RequestHandler
    return RequestHandler({
        'notification_service': notification_service,
        'user_management': user_management,
        'menu_service': menu_service,
        'voting_service': voting_service,
        'feedback_service': feedback_service,
        'recommendation_service': recommendation_service,
        'discard_item_service': discard_item_service
    })
    

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.db = get_db_connection()
        self.request_handler = create_request_handler(self.db, self.clients)
        self.start_server()

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



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("server.log"),
                            logging.StreamHandler()
                        ])
    server_config = {
        'host': 'localhost',
        'port': 12346
    }
    Server(server_config['host'], server_config['port'])
