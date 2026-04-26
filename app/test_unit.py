import unittest
import json
from app import app

class UnitTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Unit Test 1
    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Unit Test 2
    def test_home_returns_json(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertIn('status', data)

    # Unit Test 3
    def test_health_status_code(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

    # Unit Test 4
    def test_health_returns_healthy(self):
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    # Unit Test 5
    def test_hello_endpoint(self):
        response = self.app.get('/api/hello')
        self.assertEqual(response.status_code, 200)

    # Unit Test 6
    def test_hello_returns_message(self):
        response = self.app.get('/api/hello')
        data = json.loads(response.data)
        self.assertIn('message', data)

    # Unit Test 7
    def test_version_endpoint(self):
        response = self.app.get('/api/version')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
