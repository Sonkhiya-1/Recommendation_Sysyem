# client/handlers/admin_handler.py

def add_menu_item(client):
    name = input("Enter Menu Item Name: ")
    price = float(input("Enter Menu Item Price: "))
    availability = input("Enter Menu Item Availability (yes/no): ")
    dietary_category = input("Enter Dietary Category (Vegetarian/Non Vegetarian/Eggetarian): ")
    spice_level = input("Enter Spice Level (High/Medium/Low): ")
    is_sweet = input("Is the dish sweet? (Yes/No): ").lower() == 'yes'
    return {
        "action": "add_menu_item",
        "name": name,
        "price": price,
        "availability": availability,
        "dietary_category": dietary_category,
        "spice_level": spice_level,
        "is_sweet": is_sweet,
        "user_id": client.user_id,
        "role": client.role
    }

def update_menu_item(client):
    item_id = int(input("Enter Menu Item ID to Update: "))
    name = input("Enter New Name (leave empty if no change): ")
    price = input("Enter New Price (leave empty if no change): ")
    availability = input("Enter New Availability (leave empty if no change): ")
    dietary_category = input("Enter New Dietary Category (leave empty if no change): ")
    spice_level = input("Enter New Spice Level (leave empty if no change): ")
    is_sweet = input("Is the dish sweet? (Yes/No): ").lower() == 'yes'
    return {
        "action": "update_menu_item",
        "item_id": item_id,
        "name": name,
        "price": price,
        "availability": availability,
        "dietary_category": dietary_category,
        "spice_level": spice_level,
        "is_sweet": is_sweet,
        "user_id": client.user_id,
        "role": client.role
    }

def delete_menu_item(client):
    item_id = int(input("Enter Menu Item ID to Delete: "))
    return {"action": "delete_menu_item", "item_id": item_id, "user_id": client.user_id, "role": client.role}

def remove_menu_item(client):
    item_id = int(input("Enter Menu Item ID to Remove from Menu: "))
    return {"action": "remove_menu_item", "item_id": item_id, "user_id": client.user_id, "role": client.role}

def request_detailed_feedback(client):
    item_id = int(input("Enter Menu Item ID for Detailed Feedback Request: "))
    return {"action": "request_detailed_feedback", "item_id": item_id, "user_id": client.user_id, "role": client.role}

def view_discard_list(client):
    return {"action": "view_discard_list", "user_id": client.user_id, "role": client.role}

admin_actions = {
    1: lambda client: {"action": "view_menu", "user_id": client.user_id, "role": client.role},
    2: add_menu_item,
    3: update_menu_item,
    4: delete_menu_item,
    5: view_discard_list,
    6: remove_menu_item,
    7: request_detailed_feedback,
}
