from abc import ABC, abstractmethod
import logging

class Command(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class ViewMenuCommand(Command):
    def __init__(self, db):
        self.db = db

    def execute(self, data):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu_items")
            menu = cursor.fetchall()
            return {'status': 'success', 'menu': menu}
        except Exception as e:
            logging.error(f"Error in ViewMenuCommand: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve menu'}

# Add other command implementations as needed
