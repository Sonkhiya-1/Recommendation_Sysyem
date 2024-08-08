def add_menu_item(client):
    name = None
    price = None
    availability = None
    dietary_category = None
    spice_level = None
    is_sweet = None
    
    while True:
        try:
            if not name:
                name = input("Enter Menu Item Name: ").strip()
                if not name:
                    print("Error: Name is required")
                    name = None
                    continue

            if not price:
                price = input("Enter Menu Item Price: ").strip()
                try:
                    price = float(price)
                except ValueError:
                    print("Error: Price must be a number")
                    price = None
                    continue

            if not availability:
                availability = input("Enter Menu Item Availability (yes/no): ").strip().lower()
                if availability not in ['yes', 'no']:
                    print("Error: Invalid availability")
                    availability = None
                    continue

            if not dietary_category:
                dietary_category = input("Enter Dietary Category (Vegetarian/Non Vegetarian/Eggetarian): ").strip()
                if dietary_category not in ['Vegetarian', 'Non Vegetarian', 'Eggetarian']:
                    print("Error: Invalid dietary category")
                    dietary_category = None
                    continue

            if not spice_level:
                spice_level = input("Enter Spice Level (High/Medium/Low): ").strip()
                if spice_level not in ['High', 'Medium', 'Low']:
                    print("Error: Invalid spice level")
                    spice_level = None
                    continue

            if is_sweet is None:
                is_sweet = input("Is the dish sweet? (Yes/No): ").strip().lower()
                if is_sweet not in ['yes', 'no']:
                    print("Error: Invalid sweetness flag")
                    is_sweet = None
                    continue
                is_sweet = is_sweet == 'yes'

            return {
                "action": "add_menu_item",
                "name": name,
                "price": price,
                "availability": availability,
                "dietary_category": dietary_category,
                "spice_level": spice_level,
                "is_sweet": is_sweet,
                "role": client.role
            }
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

def update_menu_item(client):
    item_id = None
    name = None
    price = None
    availability = None
    dietary_category = None
    spice_level = None
    is_sweet = None
    
    while True:
        try:
            if not item_id:
                item_id = input("Enter Menu Item ID to Update: ").strip()
                try:
                    item_id = int(item_id)
                except ValueError:
                    print("Error: Item ID must be an integer")
                    item_id = None
                    continue

            if name is None:
                name = input("Enter New Name (leave empty if no change): ").strip()
                name = name if name else None

            if price is None:
                price = input("Enter New Price (leave empty if no change): ").strip()
                if price:
                    try:
                        price = float(price)
                    except ValueError:
                        print("Error: Price must be a number")
                        price = None
                        continue

            if availability is None:
                availability = input("Enter New Availability (leave empty if no change): ").strip().lower()
                if availability and availability not in ['yes', 'no']:
                    print("Error: Invalid availability")
                    availability = None
                    continue
                availability = availability if availability else None

            if dietary_category is None:
                dietary_category = input("Enter New Dietary Category (leave empty if no change): ").strip()
                if dietary_category and dietary_category not in ['Vegetarian', 'Non Vegetarian', 'Eggetarian']:
                    print("Error: Invalid dietary category")
                    dietary_category = None
                    continue
                dietary_category = dietary_category if dietary_category else None

            if spice_level is None:
                spice_level = input("Enter New Spice Level (leave empty if no change): ").strip()
                if spice_level and spice_level not in ['High', 'Medium', 'Low']:
                    print("Error: Invalid spice level")
                    spice_level = None
                    continue
                spice_level = spice_level if spice_level else None

            if is_sweet is None:
                is_sweet = input("Is the dish sweet? (Yes/No): ").strip().lower()
                if is_sweet and is_sweet not in ['yes', 'no']:
                    print("Error: Invalid sweetness flag")
                    is_sweet = None
                    continue
                is_sweet = is_sweet == 'yes' if is_sweet else None

            return {
                "action": "update_menu_item",
                "item_id": item_id,
                "name": name,
                "price": price,
                "availability": availability,
                "dietary_category": dietary_category,
                "spice_level": spice_level,
                "is_sweet": is_sweet,
                "role": client.role
            }
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

def delete_menu_item(client):
    item_id = int(input("Enter Menu Item ID to Delete: "))
    return {"action": "delete_menu_item", "item_id": item_id, "user_id": client.user_id, "role": client.role}


def request_detailed_feedback(client):
    item_id = input("Enter the Menu Item ID for which you want to request detailed feedback: ").strip()
    if not item_id.isdigit():
        print("Invalid item ID. Please enter a valid number.")
        return

    request = {
        "action": "request_detailed_feedback",
        "user_id": client.user_id,
        "role": client.role,
        "item_id": int(item_id)  # Convert item_id to an integer
    }
    response = client.send_request(request)
    if response['status'] == 'success':
        print(response['message'])
    else:
        print(f"Failed to request detailed feedback: {response['message']}")
def view_discard_list(client):
    return {"action": "view_discard_list", "user_id": client.user_id, "role": client.role}

def view_feedback_responses(client):
    request = {"action": "view_feedback_responses", "user_id": client.user_id, "role": client.role}
    response = client.send_request(request)
    if response['status'] == 'success':
        print("\nFeedback Responses:")
        for feedback in response['feedback_responses']:
            print(f"ID: {feedback['id']} | Employee: {feedback['employee_id']} | Question: {feedback['question']} | Response: {feedback['response']}")
    else:
        print(f"Failed to retrieve feedback responses: {response['message']}")

admin_actions = {
    1: lambda client: {"action": "view_menu", "user_id": client.user_id, "role": client.role},
    2: add_menu_item,
    3: update_menu_item,
    4: delete_menu_item,
    5: view_discard_list,
    6: delete_menu_item,
    7: request_detailed_feedback,
    8: view_feedback_responses,
}