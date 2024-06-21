import socket
import json
import threading
from menu_display import MenuDisplay
from request_data import RequestData
from notification_listener import NotificationListener

class Client:
    def __init__(self, host, port):
        print("Initializing client...")
        self.host = host
        self.port = port
        self.socket = self._create_socket()
        self.role = None
        self.user_id = None
        self.menu_display = MenuDisplay(self)
        self.request_data = RequestData(self)
        self.notification_listener = NotificationListener(self.socket)
        self.notification_thread = threading.Thread(target=self.notification_listener.listen_for_notifications, daemon=True)
        self.notification_thread.start()
        print("Client initialized.")

    def _create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.settimeout(5)
        return s

    def send_request(self, request):
        print(f"Sending request: {request}")
        try:
            self.socket.sendall(json.dumps(request).encode())
            print("Request sent, waiting for response...")
            response = self.socket.recv(4096).decode()
            print(f"Raw response: {response}")
            return json.loads(response)
        except socket.timeout:
            print("Socket timeout occurred while waiting for the response.")
            return {'status': 'error', 'message': 'Socket timeout'}
        except Exception as e:
            print(f"Error sending request: {e}")
            return {'status': 'error', 'message': str(e)}

    def login(self):
        print("Please log in to continue:")
        employee_id = input("Enter Employee ID: ")
        password = input("Enter Password: ")
        request = {"action": "login", "employee_id": employee_id, "password": password}
        response = self.send_request(request)
        print(f"Login response: {response}")
        if response['status'] == 'success':
            self.role = response.get('role')
            self.user_id = response.get('user_id')
            print(f"Login successful! Logged in as {self.get_role_name(self.role)}.")
            return True
        else:
            print("Login failed:", response['message'])
            return False

    def get_role_name(self, role):
        roles = {1: "Admin", 2: "Chef", 3: "Employee"}
        return roles.get(role, "Unknown")

    def main_loop(self):
        while True:
            self.menu_display.display_menu(self.role)
            try:
                action = int(input("Enter your choice: "))
                if (self.role == 1 and action == 5) or (self.role == 2 and action == 7) or (self.role == 3 and action == 6):
                    print("Logging out...")
                    break
                elif self.role == 3 and action == 4:  # View Notifications
                    response = self.send_request({"action": "view_notifications", "user_id": self.user_id})
                    if response['status'] == 'success':
                        notifications = response['notifications']
                        rollout_items = response['rollout_items']
                        if notifications:
                            print("Notifications:")
                            for notification in notifications:
                                print(f"- {notification['message']}")
                        if rollout_items:
                            print("Rollout Items:")
                            print(f"{'ID':<10}{'Name':<30}{'Price':<10}")
                            displayed_items = set()
                            for item in rollout_items:
                                if item['menu_item_id'] not in displayed_items:
                                    print(f"{item['menu_item_id']:<10}{item['name']:<30}{item['price']:<10}")
                                    displayed_items.add(item['menu_item_id'])
                            dish_id = int(input("Enter Dish ID to Vote: "))
                            meal_type = input("Enter Meal Type (breakfast/lunch/dinner): ")
                            vote_response = self.send_request({"action": "vote_for_menu_item", "dish_id": dish_id, "meal_type": meal_type, "user_id": self.user_id, "role": self.role})
                            print(f"Vote response: {vote_response}")
                    else:
                        print("Failed to retrieve notifications.")
                elif self.role == 2 and action == 4:  # View Vote Counts for Chef
                    response = self.send_request({"action": "view_vote_counts"})
                    if response['status'] == 'success':
                        vote_counts = response['vote_counts']
                        if vote_counts:
                            print("Vote Counts:")
                            for vote_count in vote_counts:
                                print(f"- {vote_count['name']} ({vote_count['meal_type']}): {vote_count['vote_count']} votes")
                    else:
                        print("Failed to retrieve vote counts.")

                request = self.request_data.get_request_data(action, self.role, self.user_id)
                if not request:
                    print("Invalid action selected. Please try again.")
                    continue

                response = self.send_request(request)
                print("Response from server:", response)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    client = Client('localhost', 12346)
    if client.login():
        client.main_loop()
    else:
        print("Exiting the program due to failed login.")
