import logging
from utils.custom_json_encoder import CustomJSONEncoder
import json

class MenuManagement:
    def __init__(self, db):
        self.db = db

    def view_menu(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu_items")
            menu = cursor.fetchall()
            menu_json = json.dumps(menu, cls=CustomJSONEncoder)
            return {'status': 'success', 'menu': json.loads(menu_json)}
        except Exception as e:
            logging.error(f"Error in view_menu: {e}")
            return {'status': 'error', 'message': 'Failed to retrieve menu'}

    def add_menu_item(self, request, client_socket):
        if request.get('role') != 1:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            name, price, availability = request['name'], request['price'], request['availability']
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO menu_items (name, price, availability) VALUES (%s, %s, %s)", (name, price, availability))
            self.db.commit()
            return {'status': 'success', 'message': 'Menu item added'}
        except Exception as e:
            logging.error(f"Error in add_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to add menu item'}

    def update_menu_item(self, request, client_socket):
        if request.get('role') != 1:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            item_id, name, price, availability = request['item_id'], request['name'], request['price'], request['availability']
            cursor = self.db.cursor()
            self._execute_update(cursor, item_id, name, price, availability)
            self.db.commit()
            return {'status': 'success', 'message': 'Menu item updated'}
        except Exception as e:
            logging.error(f"Error in update_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to update menu item'}

    def _execute_update(self, cursor, item_id, name, price, availability):
        query = "UPDATE menu_items SET"
        params = []
        if name:
            query += " name=%s,"
            params.append(name)
        if price:
            query += " price=%s,"
            params.append(price)
        if availability:
            query += " availability=%s,"
            params.append(availability)
        query = query.rstrip(',')
        query += " WHERE id=%s"
        params.append(item_id)
        cursor.execute(query, tuple(params))

    def delete_menu_item(self, request, client_socket):
        if request.get('role') != 1:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM menu_items WHERE id=%s", (request['item_id'],))
            self.db.commit()
            return {'status': 'success', 'message': 'Menu item deleted'}
        except Exception as e:
            logging.error(f"Error in delete_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to delete menu item'}
