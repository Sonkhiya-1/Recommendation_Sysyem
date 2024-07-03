import unittest
from unittest.mock import MagicMock
from server.services.voting_service import VotingService

class TestVotingService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.voting_service = VotingService(self.mock_db)

    def test_vote_for_menu_item_success(self):
        request = {'user_id': 1, 'dish_id': 2, 'meal_type': 'lunch'}
        client_socket = MagicMock()
        self.mock_db.cursor.return_value.execute.return_value = None
        self.mock_db.commit.return_value = None

        response = self.voting_service.vote_for_menu_item(request, client_socket)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['message'], 'Vote submitted')

    def test_vote_for_menu_item_failure(self):
        request = {'user_id': 1, 'dish_id': 2, 'meal_type': 'lunch'}
        client_socket = MagicMock()
        self.mock_db.cursor.side_effect = Exception("Database error")

        response = self.voting_service.vote_for_menu_item(request, client_socket)
        self.assertEqual(response['status'], 'error')
        self.assertIn('Failed to submit vote', response['message'])
