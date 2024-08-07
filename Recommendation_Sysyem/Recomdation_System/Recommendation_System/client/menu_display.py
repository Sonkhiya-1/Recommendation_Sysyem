class MenuDisplay:
    def __init__(self, client):
        self.client = client

    def display_menu(self, role):
        if role == 1:
            self._display_admin_menu()
        elif role == 2:
            self._display_chef_menu()
        elif role == 3:
            self._display_employee_menu()
        else:
            print(f"Invalid role: {role}")

    def _display_admin_menu(self):
        print("\nAdmin Actions:")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. View Discard Menu Item List")
        print("6. Remove Food Item from Menu")
        print("7. Request Detailed Feedback for Food Item")
        print("8. view feedback responses")
        print("9. Logout")

    def _display_chef_menu(self):
        print("\nChef Actions:")
        print("1. View Menu")
        print("2. Get Recommendations")
        print("3. Choose Recommendation")
        print("4. View Vote Counts")
        print("5. Send Feedback")
        print("6. Send Report")
        print("7. View Discard Menu Item List")
        print("8. Remove Food Item from Menu")
        print("9. Request Detailed Feedback for Food Item")
        print("10. view feedback responses")
        print("11. Logout")

    def _display_employee_menu(self):
        print("\nEmployee Actions:")
        print("1. View Menu")
        print("2. Vote for a Dish")
        print("3. Give Review")
        print("4. View Notifications")
        print("5. Submit Feedback")
        print("6. Update Profile")
        print("7. respond to feedback questions")
        print("8. Logout")
