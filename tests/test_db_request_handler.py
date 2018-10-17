import json
import unittest

import tests.create_test_data as test_data

from zoo_server.db_request_handler import DBRequestHandler, BadId, BadData


class TestDBRequestHandler(unittest.TestCase):

    def setUp(self):
        self.session = test_data.TestSession()
        self.handler = DBRequestHandler(self.session)
        test_data.create_all_test_data(self.session)
        self.maxDiff = None

    def tearDown(self):
        self.session.close()

    def test_get_all_monkeys(self):
        answer = self.handler.get_all_monkeys()
        expected_json = [
            {'flings_poop': 'TRUE',
             'id': 1,
             'name': 'a',
             'poop_size': 1,
             'sex': 'm',
             'zoo_id': 1},
            {'flings_poop': 'FALSE',
             'id': 2,
             'name': 'b',
             'poop_size': 2,
             'sex': 'f',
             'zoo_id': 2},
            {'flings_poop': 'FALSE',
             'id': 3,
             'name': 'c',
             'poop_size': 3,
             'sex': 'm',
             'zoo_id': 2},
        ]
        self.assertEqual(json.loads(answer[0]), expected_json)
        self.assertEqual(answer[1], 200)

    def test_get_all_zoos(self):
        answer = self.handler.get_all_zoos()
        expected = [
            {'id': 1,
             'name': 'a',
             'opens': '01:00',
             'closes': '02:00',
             'monkeys':
                 [
                     {'flings_poop': 'TRUE',
                      'id': 1,
                      'name': 'a',
                      'poop_size': 1,
                      'sex': 'm',
                      'zoo_id': 1}
                 ]
             },
            {'id': 2,
             'name': 'b',
             'opens': '03:00',
             'closes': '04:00',
             'monkeys':
                 [
                     {'flings_poop': 'FALSE',
                      'id': 2,
                      'name': 'b',
                      'poop_size': 2,
                      'sex': 'f',
                      'zoo_id': 2},
                     {'flings_poop': 'FALSE',
                      'id': 3,
                      'name': 'c',
                      'poop_size': 3,
                      'sex': 'm',
                      'zoo_id': 2},
                 ]
             }
        ]
        self.assertEqual(json.loads(answer[0]), expected)
        self.assertEqual(answer[1], 200)

    def test_get_zoo_correct(self):

        answer = self.handler.get_zoo(1)

        expected = {
            'id': 1,
            'name': 'a',
            'opens': '01:00',
            'closes': '02:00',
            'monkeys': [
                {'flings_poop': 'TRUE',
                 'id': 1,
                 'name': 'a',
                 'poop_size': 1,
                 'sex': 'm',
                 'zoo_id': 1},
            ],
        }
        self.assertEqual(json.loads(answer[0]), expected)
        self.assertEqual(answer[1], 200)

    def test_get_zoo_bad_id(self):
        self.assertRaises(BadId, self.handler.get_zoo, 1000)

    def test_get_monkey_correct(self):

        answer = self.handler.get_monkey(1)

        expected = {
            'flings_poop': 'TRUE',
            'id': 1,
            'name': 'a',
            'poop_size': 1,
            'sex': 'm',
            'zoo_id': 1
                    }
        self.assertEqual(json.loads(answer[0]), expected)
        self.assertEqual(answer[1], 200)

    def test_get_monkey_bad_id(self):
        self.assertRaises(BadId, self.handler.get_monkey, 1000)

    def test_post_zoo(self):
        to_post = {'name': 'd', 'opens': '10:00', 'closes': '11:00'}
        first_answer = self.handler.post_zoo(to_post)
        to_post['id'] = json.loads(first_answer[0])['id']
        to_post['monkeys'] = []

        self.assertEqual(json.loads(first_answer[0]), to_post)
        self.assertEqual(first_answer[1], 200)

        second_answer = self.handler.get_zoo(to_post['id'])
        self.assertEqual(first_answer, second_answer)

    def test_post_zoo_bad_data(self):

        to_post = {'oops': 1}
        self.assertRaises(BadData, self.handler.post_zoo, to_post)

        to_post = {'oops': 1, 'name': 'd', 'opens': '10:00', 'closes': '11:00'}
        self.assertRaises(BadData, self.handler.post_zoo, to_post)

        to_post = {'opens': '10:00', 'closes': '11:00'}
        self.assertRaises(BadData, self.handler.post_zoo, to_post)

    def test_post_monkey(self):
        to_post = {'name': 'd', 'sex': 'm', 'flings_poop': 'FALSE', 'poop_size': 100, 'zoo_id': 1}
        first_answer = self.handler.post_monkey(to_post)
        to_post['id'] = json.loads(first_answer[0])['id']

        self.assertEqual(json.loads(first_answer[0]), to_post)
        self.assertEqual(first_answer[1], 200)

        second_answer = self.handler.get_monkey(to_post['id'])
        self.assertEqual(first_answer, second_answer)

    def test_post_monkey_bad_data(self):
        to_post = {'oops': 'sie daysie'}
        self.assertRaises(BadData, self.handler.post_monkey, to_post)

        to_post = {'oops': 1, 'name': 'd', 'sex': 'm', 'flings_poop': 'FALSE', 'poop_size': 100, 'zoo_id': 1}
        self.assertRaises(BadData, self.handler.post_monkey, to_post)

        to_post = {'sex': 'm', 'flings_poop': 'FALSE', 'poop_size': 100, 'zoo_id': 1}
        self.assertRaises(BadData, self.handler.post_monkey, to_post)

    def test_put_zoo_total(self):
        zoo_id = 1
        current_state = json.loads(self.handler.get_zoo(zoo_id)[0])
        to_put = {"name": "q", "opens": "11:00", "closes": "12:00"}
        expected = current_state.copy()
        expected.update(**to_put)
        self.assertNotEqual(current_state, expected)

        response = self.handler.put_zoo(zoo_id, to_put)
        self.assertEqual(json.loads(response[0]), expected)
        self.assertEqual(response[1], 200)

        get_response = self.handler.get_zoo(zoo_id)
        self.assertEqual(get_response, response)

    def test_put_zoo_partial(self):
        zoo_id = 1
        current_state = json.loads(self.handler.get_zoo(zoo_id)[0])
        to_put = {"opens": "11:00", "closes": "12:00"}
        expected = current_state.copy()
        expected.update(**to_put)
        self.assertNotEqual(current_state, expected)

        response = self.handler.put_zoo(zoo_id, to_put)
        self.assertEqual(json.loads(response[0]), expected)
        self.assertEqual(response[1], 200)

        get_response = self.handler.get_zoo(zoo_id)
        self.assertEqual(get_response, response)

    def test_put_zoo_bad_id(self):
        self.assertRaises(BadId, self.handler.put_zoo, 1000, {})

    def test_put_zoo_bad_data(self):

        to_put = {'oops': 1}
        self.assertRaises(BadData, self.handler.put_zoo, 1, to_put)

        to_put = {'oops': 1, 'name': 'd', 'opens': '10:00', 'closes': '11:00'}
        self.assertRaises(BadData, self.handler.put_zoo, 1, to_put)

    def test_put_monkey_total(self):
        monkey_id = 1
        current_state = json.loads(self.handler.get_monkey(monkey_id)[0])
        to_put = {'name': 'x', 'sex': 'f', 'flings_poop': 'FALSE', 'poop_size': 1000, 'zoo_id': 2}
        expected = current_state.copy()
        expected.update(**to_put)
        self.assertNotEqual(current_state, expected)

        response = self.handler.put_monkey(monkey_id, to_put)
        self.assertEqual(json.loads(response[0]), expected)
        self.assertEqual(response[1], 200)

        get_response = self.handler.get_monkey(monkey_id)
        self.assertEqual(get_response, response)

    def test_put_monkey_partial(self):
        monkey_id = 1
        current_state = json.loads(self.handler.get_monkey(monkey_id)[0])
        to_put = {'flings_poop': 'FALSE', 'zoo_id': 2}
        expected = current_state.copy()
        expected.update(**to_put)
        self.assertNotEqual(current_state, expected)

        response = self.handler.put_monkey(monkey_id, to_put)
        self.assertEqual(json.loads(response[0]), expected)
        self.assertEqual(response[1], 200)

        get_response = self.handler.get_monkey(monkey_id)
        self.assertEqual(get_response, response)

    def test_put_monkey_bad_id(self):
        self.assertRaises(BadId, self.handler.put_monkey, 1000, {})

    def test_put_monkey_bad_data(self):
        to_put = {'oops': 'sie daysie'}
        self.assertRaises(BadData, self.handler.put_monkey, 1, to_put)

        to_put = {'oops': 1, 'name': 'd', 'sex': 'm', 'flings_poop': 'FALSE', 'poop_size': 100, 'zoo_id': 1}
        self.assertRaises(BadData, self.handler.put_monkey, 1, to_put)

    def test_delete_zoo(self):
        current_zoos = json.loads(self.handler.get_all_zoos()[0])
        response = self.handler.delete_zoo(1)
        self.assertNotEqual(json.loads(response[0]), current_zoos)
        del current_zoos[0]
        self.assertEqual(json.loads(response[0]), current_zoos)
        self.assertEqual(response[1], 200)

        self.assertRaises(BadId, self.handler.get_zoo, 1)
        self.assertRaises(BadId, self.handler.get_monkey, 1)

    def test_delete_zoo_bad_id(self):
        self.assertRaises(BadId, self.handler.delete_zoo, 100)

    def test_delete_monkey(self):
        current_zoos = json.loads(self.handler.get_all_zoos()[0])

        current_monkeys = json.loads(self.handler.get_all_monkeys()[0])
        response = self.handler.delete_monkey(1)
        self.assertNotEqual(current_monkeys, json.loads(response[0]))
        del current_monkeys[0]
        self.assertEqual(current_monkeys, json.loads(response[0]))
        self.assertEqual(response[1], 200)

        self.assertRaises(BadId, self.handler.get_monkey, 1)

        current_zoos[0]['monkeys'] = []
        self.assertEqual(json.loads(self.handler.get_all_zoos()[0]), current_zoos)

    def test_delete_monkey_bad_id(self):
        self.assertRaises(BadId, self.handler.delete_monkey, 10000)
