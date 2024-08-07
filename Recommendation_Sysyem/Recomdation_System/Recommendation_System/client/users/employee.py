def vote_for_menu_item(client):
    dish_ids = input("Enter Dish IDs to Vote for (comma separated): ").split(',')
    dish_ids = [int(dish_id.strip()) for dish_id in dish_ids]
    meal_type = input("Enter Meal Type (breakfast/lunch/dinner): ")
    return {
        "action": "vote_for_menu_item",
        "dish_ids": dish_ids,
        "meal_type": meal_type,
        "user_id": client.user_id,
        "role": client.role
    }


def give_review(client):
    dish_id = int(input("Enter Dish ID to Review: "))
    rating = int(input("Enter Rating (1-5): "))
    comment = input("Enter Comment: ")
    return {"action": "give_review", "dish_id": dish_id, "rating": rating, "comment": comment, "user_id": client.user_id, "role": client.role}

def submit_feedback(client):
    comment = input("Enter Feedback Comment: ")
    item_id = int(input("Enter Menu Item ID for Feedback: "))
    return {"action": "submit_feedback", "user_id": client.user_id, "comment": comment, "item_id": item_id, "role": client.role}

def update_profile(client):
    preferences = {
        'dietary_preference': input("Please select your dietary preference (Vegetarian/Non Vegetarian/Eggetarian): "),
        'spice_level': input("Please select your spice level (High/Medium/Low): "),
        'cuisine_preference': input("Please select your cuisine preference (North Indian/South Indian/Other): "),
        'sweet_tooth': input("Do you have a sweet tooth? (Yes/No): ").strip().lower() == 'yes'
    }
    return {"action": "update_profile", "user_id": client.user_id, "preferences": preferences}

def respond_to_feedback_questions(client):
    request = {"action": "get_feedback_questions", "user_id": client.user_id, "role": client.role}
    response = client.send_request(request)
    if response['status'] == 'success':
        questions = response['feedback_questions']
        for question in questions:
            print(f"Question: {question['question']}")
            answer = input("Your answer (or 'skip'): ")
            if answer.lower() == 'skip':
                answer = 'Skipped'
            submit_feedback_response(client, question['id'], answer)
    else:
        print(f"Failed to retrieve feedback questions: {response['message']}")

def submit_feedback_response(client, question_id, response):
    request = {
        "action": "submit_feedback_response",
        "user_id": client.user_id,
        "question_id": question_id,
        "response": response,
        "role": client.role
    }
    response = client.send_request(request)
    if response['status'] == 'success':
        print("Response submitted.")
    else:
        print(f"Failed to submit response: {response['message']}")

employee_actions = {
    1: lambda client: {"action": "view_menu"},
    2: vote_for_menu_item,
    3: give_review,
    4: lambda client: {"action": "view_notifications", "user_id": client.user_id, "role": client.role},
    5: submit_feedback,
    6: update_profile,
    7: respond_to_feedback_questions
}
