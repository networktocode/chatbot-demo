import unittest
import requests

class TestFlask(unittest.TestCase):
    def setUp(self):
        pass

    def test_404(self):
        response = requests.get('http://127.0.0.1:5030/dummy')
        self.assertTrue(response.status_code == 404)

    def test_get_not_allowed(self):
        response = requests.get('http://127.0.0.1:5030/webex-teams/webhook')
        self.assertTrue(response.status_code == 405)