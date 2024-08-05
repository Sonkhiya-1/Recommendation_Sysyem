from .base_response_handler import BaseResponseHandler

class VoteCountsHandler(BaseResponseHandler):
    @staticmethod
    def display_vote_counts(response):
        if 'vote_counts' in response:
            print("\nVote Counts for Today:")
            for vote in response['vote_counts']:
                print(f"Item: {vote['name']} | Meal Type: {vote['meal_type']} | Votes: {vote['vote_count']}")
            print("Voted for the item")
        else:
            pass
