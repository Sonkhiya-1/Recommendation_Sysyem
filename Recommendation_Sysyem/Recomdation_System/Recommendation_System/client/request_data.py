class RequestData:
    def __init__(self, client):
        self.client = client

    def get_request_data(self, action, role, user_id):
        if role == 1:
            return self._get_admin_request_data(action)
        elif role == 2:
            return self._get_chef_request_data(action, user_id)  # Ensure user_id is passed here
        elif role == 3:
            return self._get_employee_request_data(action, user_id)
        return None


    def _get_admin_request_data(self, action):
        if action == 1:
            return {"action": "view_menu"}
        elif action == 2:
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
                "is_sweet": is_sweet
            }
        elif action == 3:
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
                "is_sweet": is_sweet
            }
        elif action == 4:
            item_id = int(input("Enter Menu Item ID to Delete: "))
            return {"action": "delete_menu_item", "item_id": item_id}
        elif action == 5:
            return {"action": "view_discard_list"}
        elif action == 6:
            item_id = int(input("Enter Menu Item ID to Remove from Menu: "))
            return {"action": "remove_menu_item", "item_id": item_id}
        elif action == 7:
            item_id = int(input("Enter Menu Item ID for Detailed Feedback Request: "))
            return {"action": "request_detailed_feedback", "item_id": item_id}

    def _get_chef_request_data(self, action, user_id):  # Ensure user_id is a parameter here
        if action == 1:
            return {"action": "view_menu"}
        elif action == 2:
            return {"action": "get_recommendations", "user_id": user_id, "role": self.client.role}
        elif action == 3:
            menu_item_ids = input("Enter Menu Item IDs to Recommend (comma separated): ").split(',')
            menu_item_ids = [int(id.strip()) for id in menu_item_ids]
            return {"action": "choose_recommendations", "menu_item_ids": menu_item_ids, "user_id": user_id, "role": self.client.role}
        elif action == 4:
            return {"action": "view_vote_counts"}
        elif action == 5:
            comment = input("Enter Feedback Comment: ")
            item_id = int(input("Enter Menu Item ID for Feedback: "))
            return {"action": "send_feedback", "user_id": user_id, "comment": comment, "item_id": item_id, "role": self.client.role}
        elif action == 6:
            report = input("Enter Report: ")
            return {"action": "send_report", "report": report, "user_id": user_id, "role": self.client.role}
        elif action == 7:
            return {"action": "view_discard_list"}
        elif action == 8:
            item_id = int(input("Enter Menu Item ID to Remove from Menu: "))
            return {"action": "remove_menu_item", "item_id": item_id, "user_id": user_id, "role": self.client.role}
        elif action == 9:
            item_id = int(input("Enter Menu Item ID for Detailed Feedback Request: "))
            return {"action": "request_detailed_feedback", "item_id": item_id, "user_id": user_id, "role": self.client.role}

    def _get_employee_request_data(self, action, user_id):
        if action == 1:
            return {"action": "view_menu"}
        elif action == 2:
            dish_id = int(input("Enter Dish ID to Vote: "))
            meal_type = input("Enter Meal Type (breakfast/lunch/dinner): ")
            return {"action": "vote_for_menu_item", "dish_id": dish_id, "meal_type": meal_type, "user_id": user_id, "role": self.client.role}
        elif action == 3:
            dish_id = int(input("Enter Dish ID to Review: "))
            rating = int(input("Enter Rating (1-5): "))
            comment = input("Enter Comment: ")
            return {"action": "give_review", "dish_id": dish_id, "rating": rating, "comment": comment, "user_id": user_id, "role": self.client.role}
        elif action == 4:
            return {"action": "view_notifications", "user_id": user_id, "role": self.client.role}
        elif action == 5:
            comment = input("Enter Feedback Comment: ")
            item_id = int(input("Enter Menu Item ID for Feedback: "))
            return {"action": "submit_feedback", "user_id": user_id, "comment": comment, "item_id": item_id, "role": self.client.role}
        elif action == 6:
            preferences = {
                'dietary_preference': input("Please select your dietary preference (Vegetarian/Non Vegetarian/Eggetarian): "),
                'spice_level': input("Please select your spice level (High/Medium/Low): "),
                'cuisine_preference': input("Please select your cuisine preference (North Indian/South Indian/Other): "),
                'sweet_tooth': input("Do you have a sweet tooth? (Yes/No): ").strip().lower() == 'yes'
            }
            return {"action": "update_profile", "user_id": user_id, "preferences": preferences}