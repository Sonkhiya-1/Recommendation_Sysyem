
import logging

class RequestHandler:
    def __init__(self, services):
        self.services = services

    def handle_request(self, request, client_socket):
        action_handlers = {
            'login': self.services['user_management'].login,
            'view_menu': self.services['menu_service'].view_menu,
            'add_menu_item': self.services['menu_service'].add_menu_item,
            'update_menu_item': self.services['menu_service'].update_menu_item,
            'delete_menu_item': self.services['menu_service'].delete_menu_item,
            'get_recommendations': self.services['recommendation_service'].get_recommendations,
            'choose_recommendations': self.services['recommendation_service'].choose_recommendations,
            'view_vote_counts': self.services['voting_service'].view_vote_counts,
            'send_feedback': self.services['feedback_service'].send_feedback,
            'send_report': self.services['feedback_service'].send_report,
            'view_discard_list': self.services['discard_item_service'].view_discard_list,
            'remove_menu_item': self.services['discard_item_service'].remove_menu_item,
            'request_detailed_feedback': self.services['feedback_service'].request_detailed_feedback,
            'get_feedback_questions': self.services['feedback_service'].get_feedback_questions,
            'submit_feedback_response': self.services['feedback_service'].submit_feedback_response,
            'view_feedback_responses': self.services['feedback_service'].view_feedback_responses,
            'view_notifications': self.services['notification_service'].view_notifications,
            'vote_for_menu_item': self.services['voting_service'].vote_for_menu_item,
            'submit_feedback': self.services['feedback_service'].submit_feedback,
            'logout': self.logout
        }
        handler = action_handlers.get(request['action'], self.invalid_action)
        return handler(request, client_socket)

    def invalid_action(self, request, client_socket):
        logging.warning(f"Invalid action requested: {request['action']}")
        return {'status': 'error', 'message': 'Invalid action'}

    def logout(self, request, client_socket):
        return {'status': 'success', 'message': 'Logged out successfully'}
