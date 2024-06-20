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
                return {"action": "add_menu_item", "name": name, "price": price, "availability": availability, "role": self.role}
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
                return {"action": "get_recommendations"}
            elif action == 3:
                message = input("Enter Notification Message: ")
                return {"action": "send_notification", "message": message, "role": self.role}
            elif action == 4:
                report = input("Enter Report: ")
                return {"action": "send_report", "report": report}

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
