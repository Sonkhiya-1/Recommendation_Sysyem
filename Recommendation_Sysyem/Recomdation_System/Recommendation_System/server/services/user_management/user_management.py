import logging
from server.services.user_management.user_management_queries import get_user_by_credentials, replace_user_preferences

class UserManagement:
    def __init__(self, db, clients):
        self.db = db
        self.clients = clients

    def login(self, request, client_socket):
        employee_id = request['employee_id']
        password = request['password']
        try:
            cursor = self.db.cursor(dictionary=True)
            user = get_user_by_credentials(cursor, employee_id, password)
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
            replace_user_preferences(cursor, user_id, preferences)
            self.db.commit()
            logging.debug(f"Profile updated for user_id={user_id} with preferences={preferences}")
            return {'status': 'success', 'message': 'Profile updated successfully'}
        except Exception as e:
            logging.error(f"Error in update_profile: {e}")
            return {'status': 'error', 'message': 'Failed to update profile'}
