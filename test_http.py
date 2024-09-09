import unittest
# Import the Flask app
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    # Test that landing page responds with code: '200 OK' and response should contain the text 'Things I Can Do'
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Things I Can Do', response.data)

    # Test that blog page responds with code: '200 OK' and response should contain the text 'My first try at freelancing'
    def test_post_page(self):
        response = self.app.get('/blog/my-first-freelance-exp')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My first try at freelancing', response.data)

    # Test that a non-existent page returns '404 Not Found'
    def test_404(self):
        response = self.app.get('/non-existent-page')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
