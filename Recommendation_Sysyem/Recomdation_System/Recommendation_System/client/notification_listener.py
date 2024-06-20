import json 

class NotificationListener:
    def __init__(self, socket):
        self.socket = socket
        self.notifications = []

    def listen_for_notifications(self):
        print("Starting to listen for notifications...")
        while True:
            try:
                notification = self.socket.recv(4096).decode()
                notification_data = json.loads(notification)
                print(f"Notification received: {notification_data}")
                if notification_data.get('status') == 'notification':
                    self.notifications.append(notification_data['message'])
                    print(f"\nNotification: {notification_data['message']}")
            except Exception as e:
                print(f"Error listening for notifications: {e}")
                break

    def get_notifications(self):
        return self.notifications
