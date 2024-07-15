import logging
from datetime import datetime, timedelta

class LoginHandler:
    def __init__(self, client):
        self.client = client
        self.failed_login_attempts = {}
        self.blocked_users = {}

    def login(self):
        while True:
            employee_id = input("Enter Employee ID: ")
            password = input("Enter Password: ")

            if self.is_user_blocked(employee_id):
                print(f"User ID {employee_id} is blocked for 24 hours due to multiple failed login attempts.")
                continue

            request = {"action": "login", "employee_id": employee_id, "password": password}
            response = self.client.send_request(request)

            if response['status'] == 'success':
                role_map = {"Admin": 1, "Chef": 2, "Employee": 3}
                self.client.role = role_map.get(response.get('role'))
                self.client.user_id = response.get('user_id')
                self.failed_login_attempts[employee_id] = 0  # Reset failed attempts on successful login
                return True
            else:
                print(f"Login failed: {response['message']}")
                self.track_failed_login_attempts(employee_id)
                if self.failed_login_attempts[employee_id] >= 3:
                    self.block_user(employee_id)
                    print(f"User ID {employee_id} is blocked for 24 hours due to multiple failed login attempts.")

    def is_user_blocked(self, user_id):
        if user_id in self.blocked_users:
            block_time = self.blocked_users[user_id]
            if datetime.now() < block_time:
                return True
            else:
                del self.blocked_users[user_id]  # Unblock user after 24 hours
        return False

    def track_failed_login_attempts(self, user_id):
        if user_id not in self.failed_login_attempts:
            self.failed_login_attempts[user_id] = 0
        self.failed_login_attempts[user_id] += 1

    def block_user(self, user_id):
        self.blocked_users[user_id] = datetime.now() + timedelta(hours=24)
