import unittest
from main import get_texts  # Replace 'main' with the name of your main Python file if it's different
from unittest.mock import Mock, patch
from flask import Flask, jsonify

app = Flask(__name__)


class TestApp(unittest.TestCase):

    def test_get_texts(self):
        with app.app_context():
            result = get_texts()
            self.assertIsNotNone(result)

    @patch('main.get_texts')
    def test_get_texts_empty(self, mock_get_texts):
        with app.app_context():
            mock_get_texts.return_value = jsonify([])
            result = get_texts()
            self.assertEqual(result.get_json(), [])

    @patch('main.get_texts')
    def test_get_texts_single_entry(self, mock_get_texts):
        with app.app_context():
            mock_get_texts.return_value = jsonify([{'id': 1, 'title': 'Some Title'}])
            result = get_texts()
            print("Expected:", [{'id': 1, 'title': 'Title 1'}, {'id': 2, 'title': 'Title 2'}])
            print("Actual:", result.get_json())
            self.assertEqual(result.get_json(), [{'id': 1, 'title': 'Some Title'}])
            print("Result:", result.get_json())


    @patch('main.get_texts')
    def test_get_texts_multiple_entries(self, mock_get_texts):
        with app.app_context():
            mock_get_texts.return_value = jsonify([{'id': 1, 'title': 'Title 1'}, {'id': 2, 'title': 'Title 2'}])
            result = get_texts()
            print("Expected:", [{'id': 1, 'title': 'Title 1'}, {'id': 2, 'title': 'Title 2'}])
            print("Actual:", result.get_json())
            self.assertEqual(result.get_json(), [{'id': 1, 'title': 'Title 1'}, {'id': 2, 'title': 'Title 2'}])
            print("Result:", result.get_json())



if __name__ == '__main__':
    unittest.main()
