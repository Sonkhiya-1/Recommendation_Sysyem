from responses.base_response_handler import BaseResponseHandler

class MessageHandler(BaseResponseHandler):
    @staticmethod
    def display_message(response):
        if 'message' in response:
            print(f"\nMessage: {response['message']}")
        else:
            print("No message to display.")
