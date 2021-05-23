from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Time:', res.data)

    def test_valid_word(self):
        """Create a simple, fake board in the session, and then see if the boggle.py check_valid_word method recognizes a word on it"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["E", "A", "T", "T", "T"], 
                                 ["E", "A", "T", "T", "T"], 
                                 ["E", "A", "T", "T", "T"], 
                                 ["E", "A", "T", "T", "T"], 
                                 ["E", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=eat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """See if the word is valid on the current board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """See if the word is in the game's dictionary"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=qqqqqqqqq')
        self.assertEqual(response.json['result'], 'not-word')
