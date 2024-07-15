from .base_response_handler import BaseResponseHandler

class DiscardListHandler(BaseResponseHandler):
    @staticmethod
    def display_discard_list(response):
        if 'discard_list' in response:
            print("\nDiscard List:")
            for item in response['discard_list']:
                print(f"ID: {item['id']} | Name: {item['name']} | Rating: {item['average_rating']} | Sentiments: {item['sentiments']}")
        else:
            print("No discard items to display.")
