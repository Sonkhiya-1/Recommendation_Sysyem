import mysql.connector
from db_connection import get_db_connection

class User:
    def __init__(self, employee_id, name, role):
        self.employee_id = employee_id
        self.name = name
        self.role = role

class AuthService:
    def __init__(self):
        self.db = get_db_connection()

    def authenticate(self, employee_id, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT u.name, r.name FROM users u JOIN roles r ON u.role_id = r.id WHERE u.employee_id = %s AND u.password = %s", (employee_id, password))
        result = cursor.fetchone()
        if result:
            return User(employee_id, result[0], result[1])
        else:
            return None

if __name__ == "__main__":
    auth_service = AuthService()
    user = auth_service.authenticate('E001', 'password123')
    if user:
        print(f"Authenticated: {user.name} as {user.role}")
    else:
        print("Authentication failed")
