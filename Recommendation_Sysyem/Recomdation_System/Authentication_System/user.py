import bcrypt
from datetime import datetime

class User:
    def __init__(self, user_id, username, password_hash, role, created_at):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    @classmethod
    def from_db(cls, user_data):
        return cls(*user_data)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
