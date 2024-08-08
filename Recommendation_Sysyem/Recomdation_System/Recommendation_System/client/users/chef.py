def get_recommendations(client):
    min_items = int(input("Enter the number of recommendations per meal type: "))
    return {
        "action": "get_recommendations",
        "user_id": client.user_id,
        "role": client.role,
        "min_items": min_items
    }
    
def choose_recommendations(client):
    menu_item_ids = input("Enter Menu Item IDs to Recommend (comma separated): ").split(',')
    menu_item_ids = [int(id.strip()) for id in menu_item_ids]

    return {
        "action": "choose_recommendations",
        "menu_item_ids": menu_item_ids,
        "user_id": client.user_id,
        "role": client.role,
    }


def send_feedback(client):
    comment = input("Enter Feedback Comment: ")
    item_id = int(input("Enter Menu Item ID for Feedback: "))
    return {"action": "send_feedback", "user_id": client.user_id, "comment": comment, "item_id": item_id, "role": client.role}

def send_report(client):
    report = input("Enter Report: ")
    return {"action": "send_report", "report": report, "user_id": client.user_id, "role": client.role}

def remove_menu_item(client):
    item_id = int(input("Enter Menu Item ID to Remove from Menu: "))
    return {"action": "remove_menu_item", "item_id": item_id, "user_id": client.user_id, "role": client.role}

def request_detailed_feedback(client):
    item_id = input("Enter the Menu Item ID for which you want to request detailed feedback: ").strip()
    if not item_id.isdigit():
        print("Invalid item ID. Please enter a valid number.")
        return

    request = {
        "action": "request_detailed_feedback",
        "user_id": client.user_id,
        "role": client.role,
        "item_id": int(item_id)  # Convert item_id to an integer
    }
    response = client.send_request(request)
    if response['status'] == 'success':
        print(response['message'])
    else:
        print(f"Failed to request detailed feedback: {response['message']}")

def view_feedback_responses(client):
    request = {"action": "view_feedback_responses", "user_id": client.user_id, "role": client.role}
    response = client.send_request(request)
    if response['status'] == 'success':
        print("\nFeedback Responses:")
        for feedback in response['feedback_responses']:
            print(f"ID: {feedback['id']} | Employee: {feedback['employee_id']} | Question: {feedback['question']} | Response: {feedback['response']}")
    else:
        print(f"Failed to retrieve feedback responses: {response['message']}")

chef_actions = {
    1: lambda client: {"action": "view_menu"},
    2: lambda client: {
        "action": "get_recommendations",
        "user_id": client.user_id,
        "role": client.role,
        "min_items": int(input("Enter the number of recommendations per meal type: "))
    },
    3: choose_recommendations,
    4: lambda client: {"action": "view_vote_counts"},
    5: send_feedback,
    6: send_report,
    7: lambda client: {"action": "view_discard_list"},
    8: remove_menu_item,
    9: request_detailed_feedback,
    10: view_feedback_responses,
}