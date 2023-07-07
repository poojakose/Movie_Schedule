import unittest
from flask import Flask
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Schedule', response.data)

    def test_movies_route(self):
        response = self.app.post('/movies', data={'genre': 'Drama'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Drama', response.data)

    def test_invalid_route(self):
        response = self.app.get('/invalid')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
