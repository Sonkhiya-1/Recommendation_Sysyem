import unittest
from unittest.mock import MagicMock, patch
from client.client import Client
import json

class TestClient(unittest.TestCase):
    @patch('client.client.create_socket')
    def setUp(self, mock_create_socket):
        self.mock_socket = MagicMock()
        mock_create_socket.return_value = self.mock_socket
        self.client = Client('localhost', 12346)

    def test_login_success(self):
        self.mock_socket.recv.return_value = json.dumps({'status': 'success', 'role': 1, 'user_id': 101}).encode()
        with patch('builtins.input', side_effect=['123', 'password']):
            result = self.client.login()
            self.assertTrue(result)
            self.assertEqual(self.client.role, 1)
            self.assertEqual(self.client.user_id, 101)

    def test_login_failure(self):
        self.mock_socket.recv.return_value = json.dumps({'status': 'error', 'message': 'Invalid credentials'}).encode()
        with patch('builtins.input', side_effect=['123', 'wrongpassword']):
            result = self.client.login()
            self.assertFalse(result)
