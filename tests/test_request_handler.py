import json
import unittest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import tests.create_test_data as test_data

from zoo_server.request_handler import RequestHandler


test_engine = create_engine("mysql://{}@localhost/{}".format(test_data.USER, test_data.TEST_DB),
                            encoding='latin1')


TestSession = sessionmaker(bind=test_engine)


from pprint import pprint


class TestRequestHandler(unittest.TestCase):

    @patch('zoo_server.request_handler.Session', TestSession)
    def setUp(self):
        self.handler = RequestHandler()
        self.session = TestSession()
        test_data.main()

    def tearDown(self):
        self.handler.close_connection()
        self.session.close()

    def test_get_all_monkeys(self):
        answer = self.handler.get_all_monkeys()
        expected_json = [
            {'flings_poop': 'TRUE',
             'id': 1,
             'name': 'Dopey',
             'poop_size': 12,
             'sex': 'm',
             'zoo_name': "Wacky Zachy's Monkey Attacky"},
            {'flings_poop': 'FALSE',
             'id': 2,
             'name': 'Sneezy',
             'poop_size': 8,
             'sex': 'f',
             'zoo_name': 'The Boringest Zoo On Earth'},
            {'flings_poop': 'TRUE',
             'id': 3,
             'name': 'Wheezy',
             'poop_size': 25,
             'sex': 'm',
             'zoo_name': 'The Boringest Zoo On Earth'},
            {'flings_poop': 'TRUE',
             'id': 4,
             'name': 'Doc',
             'poop_size': 100,
             'sex': 'f',
             'zoo_name': "Wacky Zachy's Monkey Attacky"}
        ]
        self.assertEqual(json.loads(answer[0]), expected_json)
        self.assertEqual(answer[1], 200)

    def test_get_all_zoos(self):
        answer = self.handler.get_all_zoos()
        expected = [
            {'closes': '13:15',
             'monkeys': [
                 {'flings_poop': 'TRUE',
                  'id': 1,
                  'name': 'Dopey',
                  'poop_size': 12,
                  'sex': 'm',
                  'zoo_name': "Wacky Zachy's Monkey Attacky"},
                 {'flings_poop': 'TRUE',
                  'id': 4,
                  'name': 'Doc',
                  'poop_size': 100,
                  'sex': 'f',
                  'zoo_name': "Wacky Zachy's Monkey Attacky"}],
             'name': "Wacky Zachy's Monkey Attacky",
             'opens': '13:00'},
            {'closes': '17:00',
             'monkeys': [
                 {'flings_poop': 'FALSE',
                  'id': 2,
                  'name': 'Sneezy',
                  'poop_size': 8,
                  'sex': 'f',
                  'zoo_name': 'The Boringest Zoo On Earth'},
                 {'flings_poop': 'TRUE',
                  'id': 3,
                  'name': 'Wheezy',
                  'poop_size': 25,
                  'sex': 'm',
                  'zoo_name': 'The Boringest Zoo On Earth'}
             ],
             'name': 'The Boringest Zoo On Earth',
             'opens': '08:00'}
        ]
        self.assertEqual(json.loads(answer[0]), expected)
        self.assertEqual(answer[1], 200)

