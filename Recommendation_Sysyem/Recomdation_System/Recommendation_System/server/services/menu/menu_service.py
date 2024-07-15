import logging
import json
from server.services.menu.menu_queries import get_menu, insert_menu_item, update_menu_item, delete_menu_item
from utils.custom_json_encoder import CustomJSONEncoder

class MenuService:
    def __init__(self, db, notification_service):
        self.db = db
        self.notification_service = notification_service

    def view_menu(self, request, client_socket):
        try:
            cursor = self.db.cursor(dictionary=True)
            menu = get_menu(cursor)
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
            dietary_category = request['dietary_category']
            spice_level = request['spice_level']
            is_sweet = request['is_sweet']
            cursor = self.db.cursor()
            insert_menu_item(cursor, name, price, availability, dietary_category,spice_level, is_sweet)
            self.db.commit()
            self.notification_service.send_notification_to_all_employees(f"New menu item added: {name}")
            return {'status': 'success', 'message': 'Menu item added'}
        except Exception as e:
            logging.error(f"Error in add_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to add menu item'}

    def update_menu_item(self, request, client_socket):
        if request.get('role') != 1:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            item_id, name, price, availability = request['item_id'], request['name'], request['price'], request['availability']
            dietary_category = request['dietary_category']
            spice_level = request['spice_level']
            is_sweet = request['is_sweet']
            cursor = self.db.cursor()
            update_menu_item(cursor, item_id, name, price, availability, dietary_category, spice_level, is_sweet)
            self.db.commit()
            self.notification_service.send_notification_to_all_employees(f"Menu item updated: ID {item_id}")
            return {'status': 'success', 'message': 'Menu item updated'}
        except Exception as e:
            logging.error(f"Error in update_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to update menu item'}

    def delete_menu_item(self, request, client_socket):
        if request.get('role') != 1:
            return {'status': 'error', 'message': 'Permission denied'}
        try:
            item_id = request['item_id']
            cursor = self.db.cursor()
            delete_menu_item(cursor, request['item_id'])
            self.db.commit()
            self.notification_service.send_notification_to_all_employees(f"Menu item deleted: ID {request['item_id']}")
            return {'status': 'success', 'message': 'Menu item deleted'}
        except Exception as e:
            logging.error(f"Error in delete_menu_item: {e}")
            return {'status': 'error', 'message': 'Failed to delete menu item'}
