import logging

class UserManagement:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def login(self, request, client_socket):
        employee_id = request['employee_id']
        password = request['password']
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE employee_id=%s AND password=%s", (employee_id, password))
            user = cursor.fetchone()
            if user:
                self.clients[client_socket] = user['role']
                return {'status': 'success', 'role': user['role'], 'user_id': user['id']}
            else:
                return {'status': 'error', 'message': 'Invalid credentials'}
        except Exception as e:
            logging.error(f"Error in login: {e}")
            return {'status': 'error', 'message': 'Failed to login'}

    def update_profile(self, request, client_socket):
        user_id = request['user_id']
        preferences = request['preferences']  # Should be a dictionary of preference data
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                REPLACE INTO user_preferences (user_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, preferences['dietary_preference'], preferences['spice_level'], preferences['cuisine_preference'], preferences['sweet_tooth'])
            )
            self.db.commit()
            logging.debug(f"Profile updated for user_id={user_id} with preferences={preferences}")
            return {'status': 'success', 'message': 'Profile updated successfully'}
        except Exception as e:
            logging.error(f"Error in update_profile: {e}")
            return {'status': 'error', 'message': 'Failed to update profile'}