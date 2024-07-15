
from client.users.admin import admin_actions
from client.users.chef import chef_actions
from client.users.employee import employee_actions

class RequestData:
    def __init__(self, client):
        self.client = client

    def get_request_data(self, action, role, user_id):
        if role == 1:
            return self._handle_action(admin_actions, action, self.client)
        elif role == 2:
            return self._handle_action(chef_actions, action, self.client)
        elif role == 3:
            return self._handle_action(employee_actions, action, self.client)
        else:
            raise ValueError("Invalid role")

    def _handle_action(self, actions, action, client):
        action_func = actions.get(action, self._invalid_action)
        return action_func(client)

    def _invalid_action(self, client):
        print("Invalid action selected. Please try again.")
        return None


