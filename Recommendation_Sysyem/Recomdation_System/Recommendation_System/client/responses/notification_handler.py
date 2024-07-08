# class NotificationHandler:
#     @staticmethod
#     def display_notifications(response):
#         if 'notifications' in response:
#             print("\nNotifications:")
#             for notification in response['notifications']:
#                 print(f"- {notification['message']}")
            
#             if 'rollout_items' in response and response['rollout_items']:
#                 print("\nRollout Items:")
#                 for item in response['rollout_items']:
#                     print(f"Item: {item['menu_item_id']} | {item['name']} | Price: {item['price']} | Time: {item['timestamp']}")
#         else:
#             print("No notifications to display.")

class NotificationHandler:
    @staticmethod
    def display_notifications(response):
        if 'notifications' in response:
            print("\nNotifications:")
            for notification in response['notifications']:
                print(f"- {notification['message']}")
            
            if 'rollout_items' in response and response['rollout_items']:
                # Sort the rollout items based on user preferences
                sorted_rollout_items = response['rollout_items']

                print("\nRollout Items:")
                for item in sorted_rollout_items:
                    print(f"Item: {item['menu_item_id']} | {item['name']} | Price: {item['price']} | Time: {item['timestamp']}")
        else:
            print("No notifications to display.")
