from .base_response_handler import BaseResponseHandler

class RecommendationsHandler(BaseResponseHandler):
    @staticmethod
    def display_recommendations(response):
        if 'recommendations' in response:
            print("\nRecommendations:")
            meal_types = {'breakfast': [], 'lunch': [], 'dinner': []}
            for item in response['recommendations']:
                meal_types[item['meal_type']].append(item)

            min_items = response.get('min_items', 3)
            for meal_type, items in meal_types.items():
                if items:
                    print(f"\n{meal_type.capitalize()} Recommendations:")
                    for item in items[:min_items]:
                        print(f"ID: {item['id']} | Name: {item['name']} | Price: {item['price']} | Average Rating: {item['average_rating']} | Meal Type: {item['meal_type']}")
   
        else:
            pass