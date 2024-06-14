import mysql.connector
from config import Config
from user import User

class DBFactory:
    def __init__(self):
        params = Config.get_mysql_connection_params()
        self.conn = mysql.connector.connect(**params)
        self.cursor = self.conn.cursor()

    def register_user(self, username, password, role):
        password_hash = User.hash_password(password).decode('utf-8')
        query = "INSERT INTO Users (Username, PasswordHash, Role) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, password_hash, role))
        self.conn.commit()

    def get_user_by_username(self, username):
        query = "SELECT UserID, Username, PasswordHash, Role, CreatedAt FROM Users WHERE Username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()
