import json
import unittest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import tests.create_test_data as test_data

from zoo_server.db_request_handler import DBRequestHandler


def create_test_session(host='localhost'):
    test_engine = create_engine("mysql://{}@{}/{}".format(test_data.USER, host,test_data.TEST_DB),
                                encoding='latin1')
    return sessionmaker(bind=test_engine)()


from pprint import pprint


class TestDBRequestHandler(unittest.TestCase):

    @patch('zoo_server.db_request_handler.create_session', create_test_session)
    def setUp(self):
        self.handler = DBRequestHandler()
        self.session = create_test_session()
        test_data.main()
        self.maxDiff = None

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
             'zoo_name': "Wacky Zachy's Monkey Attacky",
             'zoo_id': 1},
            {'flings_poop': 'FALSE',
             'id': 2,
             'name': 'Sneezy',
             'poop_size': 8,
             'sex': 'f',
             'zoo_name': 'The Boringest Zoo On Earth',
             'zoo_id': 2},
            {'flings_poop': 'TRUE',
             'id': 3,
             'name': 'Wheezy',
             'poop_size': 25,
             'sex': 'm',
             'zoo_name': 'The Boringest Zoo On Earth',
             'zoo_id': 2},
            {'flings_poop': 'TRUE',
             'id': 4,
             'name': 'Doc',
             'poop_size': 100,
             'sex': 'f',
             'zoo_name': "Wacky Zachy's Monkey Attacky",
             'zoo_id': 1}
        ]
        self.assertEqual(json.loads(answer[0]), expected_json)
        self.assertEqual(answer[1], 200)

    def test_get_all_zoos(self):
        answer = self.handler.get_all_zoos()
        expected = [
            {'id': 1,
             'closes': '13:15',
             'monkeys': [
                 {'flings_poop': 'TRUE',
                  'id': 1,
                  'name': 'Dopey',
                  'poop_size': 12,
                  'sex': 'm',
                  'zoo_name': "Wacky Zachy's Monkey Attacky",
                  'zoo_id': 1},
                 {'flings_poop': 'TRUE',
                  'id': 4,
                  'name': 'Doc',
                  'poop_size': 100,
                  'sex': 'f',
                  'zoo_name': "Wacky Zachy's Monkey Attacky",
                  'zoo_id': 1}],
             'name': "Wacky Zachy's Monkey Attacky",
             'opens': '13:00'},
            {'id': 2,
             'closes': '17:00',
             'monkeys': [
                 {'flings_poop': 'FALSE',
                  'id': 2,
                  'name': 'Sneezy',
                  'poop_size': 8,
                  'sex': 'f',
                  'zoo_name': 'The Boringest Zoo On Earth',
                  'zoo_id': 2},
                 {'flings_poop': 'TRUE',
                  'id': 3,
                  'name': 'Wheezy',
                  'poop_size': 25,
                  'sex': 'm',
                  'zoo_name': 'The Boringest Zoo On Earth',
                  'zoo_id': 2}
             ],
             'name': 'The Boringest Zoo On Earth',
             'opens': '08:00'}
        ]
        self.assertEqual(json.loads(answer[0]), expected)
        self.assertEqual(answer[1], 200)

