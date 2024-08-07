from .base_response_handler import BaseResponseHandler

class NotificationHandler(BaseResponseHandler):
    @staticmethod
    def display_notifications(response):
        if 'notifications' in response:
            print("\nNotifications:")
            for notification in response['notifications']:
                print(f"- {notification['message']}")

            if 'rollout_items' in response and response['rollout_items']:
                sorted_rollout_items = response['rollout_items']
                print("\nRollout Items:")
                for item in sorted_rollout_items:
                    print(f"Item: {item['menu_item_id']} | {item['name']} | Price: {item['price']} | Meal Type: {item['meal_type']} | Time: {item['timestamp']}")
        else:
            pass
