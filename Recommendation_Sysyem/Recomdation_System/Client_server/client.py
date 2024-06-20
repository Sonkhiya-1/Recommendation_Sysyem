# import socket
# import json

# class Client:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.connect((self.host, self.port))

#     def send_request(self, request):
#         print(f"Sending request: {json.dumps(request)}")
#         self.socket.sendall(json.dumps(request).encode())
#         response = self.socket.recv(1024).decode()
#         if not response:
#             print("Received empty response")
#             return {'status': 'error', 'message': 'Empty response from server'}
#         print(f"Received response: {response}")
#         return json.loads(response)

#     def login(self, employee_id, password):
#         request = {'action': 'login', 'employee_id': employee_id, 'password': password}
#         return self.send_request(request)

#     def view_menu(self):
#         request = {'action': 'view_menu'}
#         return self.send_request(request)

#     def add_menu_item(self, name, price, availability, role):
#         request = {'action': 'add_menu_item', 'name': name, 'price': price, 'availability': availability, 'role': role}
#         return self.send_request(request)

#     def get_recommendations(self, role):
#         request = {'action': 'get_recommendations', 'role': role}
#         return self.send_request(request)

#     def send_notification(self, user_id, message, role):
#         request = {'action': 'send_notification', 'user_id': user_id, 'message': message, 'role': role}
#         return self.send_request(request)

#     def rate_menu_item(self, user_id, menu_item_id, rating, comment, role):
#         request = {'action': 'rate_menu_item', 'user_id': user_id, 'menu_item_id': menu_item_id, 'rating': rating, 'comment': comment, 'role': role}
#         return self.send_request(request)

# if __name__ == "__main__":
#     client = Client('localhost', 12345)
#     response = client.login('E001', 'password123')
#     print(response)

#     if response['role'] == 1:
#         print(client.view_menu())
#         print(client.add_menu_item('Pizza', 12.99, 'yes', response['role']))
#     elif response['role'] == 2:
#         print(client.view_menu())
#         print(client.get_recommendations(response['role']))
#         print(client.send_notification(3, 'Try our new specials!', response['role']))
#     elif response['role'] == 3:
#         print(client.view_menu())
#         print(client.rate_menu_item(3, 2, 5, 'Loved the Pizza!', response['role']))


import socket
import json

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.role = None

    def send_request(self, request):
        try:
            self.socket.sendall(json.dumps(request).encode())
            response = self.socket.recv(4096).decode()
            return json.loads(response)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def login(self):
        print("Please log in to continue:")
        employee_id = input("Enter Employee ID: ")
        password = input("Enter Password: ")
        request = {"action": "login", "employee_id": employee_id, "password": password}
        response = self.send_request(request)
        if response['status'] == 'success':
            self.role = response['role']
            print(f"Login successful! Logged in as {self.get_role_name(self.role)}.")
        else:
            print("Login failed:", response['message'])
            return False
        return True

    def get_role_name(self, role):
        roles = {1: "Admin", 2: "Chef", 3: "Employee"}
        return roles.get(role, "Unknown")

    def display_menu(self):
        if self.role == 1:
            self.display_admin_menu()
        elif self.role == 2:
            self.display_chef_menu()
        elif self.role == 3:
            self.display_employee_menu()

    def display_admin_menu(self):
        print("\nAdmin Actions:")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. Logout")

    def display_chef_menu(self):
        print("\nChef Actions:")
        print("1. View Menu")
        print("2. Get Recommendations")
        print("3. Send Notification")
        print("4. Send Report")
        print("5. Logout")

    def display_employee_menu(self):
        print("\nEmployee Actions:")
        print("1. View Menu")
        print("2. Vote for a Dish")
        print("3. Give Review")
        print("4. Logout")

    def get_request_data(self, action):
        if self.role == 1:  # Admin
            if action == 1:
                return {"action": "view_menu"}
            elif action == 2:
                name = input("Enter Menu Item Name: ")
                price = float(input("Enter Menu Item Price: "))
                availability = input("Enter Menu Item Availability (yes/no): ")
                return {"action": "add_menu_item", "name": name, "price": price, "availability": availability}
            elif action == 3:
                item_id = int(input("Enter Menu Item ID to Update: "))
                name = input("Enter New Name (leave empty if no change): ")
                price = input("Enter New Price (leave empty if no change): ")
                availability = input("Enter New Availability (leave empty if no change): ")
                return {"action": "update_menu_item", "item_id": item_id, "name": name, "price": price, "availability": availability}
            elif action == 4:
                item_id = int(input("Enter Menu Item ID to Delete: "))
                return {"action": "delete_menu_item", "item_id": item_id}

        elif self.role == 2:  # Chef
            if action == 1:
                return {"action": "view_menu"}
            elif action == 2:
                return {"action": "get_recommendations", "role": self.role}
            elif action == 3:
                message = input("Enter Notification Message: ")
                return {"action": "send_notification", "message": message, "role": self.role}
            elif action == 4:
                report = input("Enter Report: ")
                return {"action": "send_report", "report": report, "role": self.role}

        elif self.role == 3:  # Employee
            if action == 1:
                return {"action": "view_menu"}
            elif action == 2:
                dish_id = int(input("Enter Dish ID to Vote: "))
                return {"action": "vote_for_dish", "dish_id": dish_id, "role": self.role}
            elif action == 3:
                dish_id = int(input("Enter Dish ID to Review: "))
                rating = int(input("Enter Rating (1-5): "))
                comment = input("Enter Comment: ")
                return {"action": "give_review", "dish_id": dish_id, "rating": rating, "comment": comment, "role": self.role}

        return None

    def main_loop(self):
        while True:
            self.display_menu()
            try:
                action = int(input("Enter your choice: "))
                if action == 5 and self.role == 1:  # Admin Logout
                    print("Logging out...")
                    break
                if action == 5 and self.role == 2:  # Chef Logout
                    print("Logging out...")
                    break
                if action == 4 and self.role == 3:  # Employee Logout
                    print("Logging out...")
                    break

                request = self.get_request_data(action)
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
