from responses.base_response_handler import BaseResponseHandler

class MenuHandler(BaseResponseHandler):
    @staticmethod
    def display_menu(response):
        if 'menu' in response:
            print("\nMenu Items:")
            for item in response['menu']:
                print(f"ID: {item['id']} | Name: {item['name']} | Price: {item['price']} | Availability: {item['availability']}")
        else:
            print("No menu items to display.")
