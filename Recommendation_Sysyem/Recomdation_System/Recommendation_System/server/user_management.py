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
