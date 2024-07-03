import unittest
from unittest.mock import MagicMock, patch
from server.server import Server

class TestServer(unittest.TestCase):
    @patch('server.server.get_db_connection')
    @patch('server.server.RequestHandler')
    def setUp(self, mock_request_handler, mock_get_db_connection):
        self.mock_db_connection = MagicMock()
        mock_get_db_connection.return_value = self.mock_db_connection
        self.mock_request_handler = mock_request_handler.return_value
        self.server = Server('localhost', 12346)

    def test_server_initialization(self):
        self.assertEqual(self.server.host, 'localhost')
        self.assertEqual(self.server.port, 12346)
        self.assertIsNotNone(self.server.db)
        self.assertIsNotNone(self.server.request_handler)
