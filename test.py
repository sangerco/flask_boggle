from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
            """ Test response code
                check that board is created
                check that High Score is created
                check that timer is created
            """
            with self.client:
                resp = self.client.get('/')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<table id="board_board">', html)
                self.assertIn('<b>High Score:</b>', html)
                self.assertIn('<span class="timer">60</span>', html)

    def test_for_word_not_on_board(self):
        with app.test_client() as client:
            resp = client.get('/check-word?word=abracadabra')
            self.assertEqual(resp.json['result'], "not-on-board")

    def test_for_not_a_word(self):
        with app.test_client() as client:
            resp = client.get('/check-word?word=notaword')
            self.assertEqual(resp.json['result'], "not-word")

