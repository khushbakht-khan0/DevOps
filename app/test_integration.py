import unittest
import json
from app import app

class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Integration Test 1
    def test_health_check_full_response(self):
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'flask-app')

    # Integration Test 2
    def test_version_full_response(self):
        response = self.app.get('/api/version')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('version', data)
        self.assertIn('app', data)
        self.assertEqual(data['version'], '1.0.0')

    # Integration Test 3
    def test_content_type_is_json(self):
        response = self.app.get('/health')
        self.assertIn('application/json', response.content_type)

if __name__ == '__main__':
    unittest.main()
