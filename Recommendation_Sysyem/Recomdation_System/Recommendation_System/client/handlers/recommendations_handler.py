from .base_response_handler import BaseResponseHandler

class RecommendationsHandler(BaseResponseHandler):
    @staticmethod
    def display_recommendations(response):
        if 'recommendations' in response:
            print("\nRecommendations:")
            for item in response['recommendations']:
                print(f"ID: {item['id']} | Name: {item['name']} | Price: {item['price']} | Average Rating: {item['average_rating']}")
        else:
            print("No recommendations to display.")
