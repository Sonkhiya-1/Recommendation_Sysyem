from .menu_handler import MenuHandler
from .discard_list_handler import DiscardListHandler
from .message_handler import MessageHandler
from .recommendations_handler import RecommendationsHandler
from .vote_counts_handler import VoteCountsHandler
from .notification_handler import NotificationHandler

def initialize_action_handlers(client):
    return {
        1: MenuHandler.display_menu,
        2: {
            2: RecommendationsHandler.display_recommendations,  # Chef
            3: VoteCountsHandler.display_vote_counts,           # Employee
        },
        3: {
            2: RecommendationsHandler.display_recommendations,  # Chef
        },
        4: {
            2: VoteCountsHandler.display_vote_counts,           # Chef
            3: NotificationHandler.display_notifications,       # Employee
        },
        5: {
            1:DiscardListHandler.display_discard_list,          #Admin
            2: MessageHandler.display_message,                  # Chef
        },
        6: {
            1: MessageHandler.display_message,
            2: MessageHandler.display_message,                  # Chef
            3: client.handle_profile_update_response,           # Employee (Profile Update)
        },
        7: DiscardListHandler.display_discard_list,
        8: MessageHandler.display_message,
        9: MessageHandler.display_message,
        10: client._logout_handler
    }
