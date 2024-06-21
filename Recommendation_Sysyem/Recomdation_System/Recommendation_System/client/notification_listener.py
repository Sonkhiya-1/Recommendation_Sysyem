import json

class NotificationListener:
    def __init__(self, socket):
        self.socket = socket

    def listen_for_notifications(self):
        print("Starting to listen for notifications...")
        buffer = ""
        while True:
            try:
                data = self.socket.recv(4096).decode()
                if not data:
                    continue

                buffer += data
                while True:
                    try:
                        notification, buffer = self._extract_json(buffer)
                        if notification:
                            notification_data = json.loads(notification)
                            print(f"Notification received: {notification_data}")
                            if notification_data.get('status') == 'notification':
                                print(f"\nNotification: {notification_data['message']}")
                        else:
                            break
                    except json.JSONDecodeError:
                        break
            except Exception as e:
                print(f"Error listening for notifications: {e}")
                break

    def _extract_json(self, buffer):
        brace_count = 0
        start = 0
        for i, char in enumerate(buffer):
            if char == '{':
                if brace_count == 0:
                    start = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return buffer[start:i + 1], buffer[i + 1:]
        return None, buffer
