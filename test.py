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
            res = self.client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<table id="board_board">', html)
            self.assertIn('<b>High Score:</b>', html)
            self.assertIn('<span class="timer"></span>', html)

    def test_for_word_not_on_board(self):
        """ Test for word that cannot be on the board
            Should get proper code
        """
        with app.test_client() as client:
            self.client.get('/')
            res = self.client.get('/check_word?word=abracadabra')
            html = res.get_data(as_text=True)
            # self.assertIn('<p class="msg err">abracadabra is not on the board!</p>', html)   
            self.assertEqual(res.json['result'], "not-on-board")




    def test_for_not_a_word(self):
        """ Test for nonsense word
            Should get proper code
        """
        with app.test_client() as client:
            self.client.get('/')
            res = self.client.get('/check_word?word=notaword')
            html = res.get_data(as_text=True)
            # self.assertIn('<p class="msg err">notaword is not a valid word!</p>', html) 
            self.assertEqual(res.json['result'], "not-word")

