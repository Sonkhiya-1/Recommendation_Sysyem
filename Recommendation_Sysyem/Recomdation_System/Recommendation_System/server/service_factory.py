from services.feedback_service import FeedbackService
from services.menu_service import MenuService
from services.notification_service import NotificationService
from services.recommendation_service import RecommendationService
from services.voting_service import VotingService
from services.discard_item_service import DiscardItemService
from user_management import UserManagement

def create_request_handler(db, clients):

    notification_service = NotificationService(db, clients)
    user_management = UserManagement(db, clients)
    menu_service = MenuService(db, notification_service)
    voting_service = VotingService(db)
    feedback_service = FeedbackService(db)
    recommendation_service = RecommendationService(db, clients)
    discard_item_service = DiscardItemService(db, notification_service)


    from server.request_handler import RequestHandler

 
    return RequestHandler({
        'notification_service': notification_service,
        'user_management': user_management,
        'menu_service': menu_service,
        'voting_service': voting_service,
        'feedback_service': feedback_service,
        'recommendation_service': recommendation_service,
        'discard_item_service': discard_item_service
    })
