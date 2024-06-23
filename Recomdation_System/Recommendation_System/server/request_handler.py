from user_management import UserManagement
from menu_management import MenuManagement
from service.notification_service import NotificationService
from service.voting_service import VotingService
from service.feedback_service import FeedbackService
from service.recommendation_service import RecommendationService

class RequestHandler:
    def __init__(self, db, clients):
        self.notification_service = NotificationService(db, clients)
        self.user_management = UserManagement(db, clients)
        self.menu_management = MenuManagement(db, self.notification_service)
        self.voting_service = VotingService(db)
        self.feedback_service = FeedbackService(db)
        self.recommendation_service = RecommendationService(db, clients)

    def handle_request(self, request, client_socket):
        action_handlers = {
            'login': self.user_management.login,
            'view_menu': self.menu_management.view_menu,
            'add_menu_item': self.menu_management.add_menu_item,
            'update_menu_item': self.menu_management.update_menu_item,
            'delete_menu_item': self.menu_management.delete_menu_item,
            'get_recommendations': self.recommendation_service.get_recommendations,
            'choose_recommendations': self.recommendation_service.choose_recommendations,
            'view_vote_counts': self.voting_service.view_vote_counts,
            'send_feedback': self.feedback_service.send_feedback,
            'send_notification': self.notification_service.send_notification_to_all_employees,
            'view_notifications': self.notification_service.view_notifications,
            'vote_for_menu_item': self.voting_service.vote_for_menu_item,
            #'give_review': self.feedback_service.give_review,
            'submit_feedback': self.feedback_service.submit_feedback,
            #'send_report': self.feedback_service.send_report
        }
        handler = action_handlers.get(request['action'], self.invalid_action)
        return handler(request, client_socket)

    def invalid_action(self, request, client_socket):
        return {'status': 'error', 'message': 'Invalid action'}
