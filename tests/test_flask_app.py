import unittest
from unittest.mock import patch

import json

from zoo_server import flask_app
from zoo_server.db_request_handler import DBRequestHandler
from tests.create_test_data import create_all_test_data, TestSession


class TestFlaskApp(unittest.TestCase):

    session_patch_str = 'zoo_server.data_base_session.DataBaseSession'

    methods = [key for key in DBRequestHandler.__dict__.keys() if not key.startswith('__')]

    def setUp(self):
        self.app = flask_app.app.test_client()
        flask_app.app.testing = True
        create_all_test_data(TestSession())

    def test_all_monkeys_get(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.get('/monkeys/')
            expected_json = [
                {'flings_poop': 'TRUE',
                 'id': 1,
                 'name': 'a',
                 'poop_size': 1,
                 'sex': 'm',
                 'zoo_name': "a",
                 'zoo_id': 1},
                {'flings_poop': 'FALSE',
                 'id': 2,
                 'name': 'b',
                 'poop_size': 2,
                 'sex': 'f',
                 'zoo_name': 'b',
                 'zoo_id': 2},
                {'flings_poop': 'FALSE',
                 'id': 3,
                 'name': 'c',
                 'poop_size': 3,
                 'sex': 'm',
                 'zoo_name': 'b',
                 'zoo_id': 2},
            ]
            self.assertEqual(json.loads(response.data), expected_json)
            self.assertEqual(response.status_code, 200)

    def test_all_monkeys_post(self):
        with patch(self.session_patch_str, TestSession):
            json_data = {"name": "d", 'flings_poop': 'TRUE', 'poop_size': 4, 'sex': 'm', 'zoo_id': 1}
            response = self.app.post('/monkeys/', json=json_data)

            response_json = json.loads(response.data)
            expected = json_data.copy()
            expected['zoo_name'] = 'a'
            expected['id'] = response_json['id']
            self.assertEqual(response_json, expected)
            self.assertEqual(response.status_code, 200)

    def test_all_monkeys_post_bad_data(self):
        with patch(self.session_patch_str, TestSession):
            bad_data = {'ooop': 1}
            response = self.app.post('/monkeys/', json=bad_data)

            response_json = json.loads(response.data)
            expected = {
                'error': 400,
                'error_type': 'BadData',
                'title': 'bad request',
                'text': response_json['text']
            }
            self.assertEqual(response_json, expected)
            self.assertEqual(response.status_code, 400)

    def test_all_monkeys_head(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.head('/monkeys/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"")

    def test_all_zoos_get(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.get('/zoos/')
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
                          'zoo_name': "a",
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
                          'zoo_name': 'b',
                          'zoo_id': 2},
                         {'flings_poop': 'FALSE',
                          'id': 3,
                          'name': 'c',
                          'poop_size': 3,
                          'sex': 'm',
                          'zoo_name': 'b',
                          'zoo_id': 2},
                     ]
                 }
            ]
            self.assertEqual(json.loads(response.data), expected)
            self.assertEqual(response.status_code, 200)

    def test_all_zoos_post(self):
        with patch(self.session_patch_str, TestSession):
            json_data = {'name': 'x', 'opens': '12:00', 'closes': '10:00'}
            response = self.app.post('/zoos/', json=json_data)
            response_json = json.loads(response.data)
            json_data['id'] = response_json['id']
            json_data['monkeys'] = []
            self.assertEqual(json_data, response_json)
            self.assertEqual(response.status_code, 200)

    def test_all_zoo_post_bad_data(self):
        with patch(self.session_patch_str, TestSession):
            bad_data = {'oops': 'a'}
            response = self.app.post('/zoos/', json=bad_data)
            response_json = json.loads(response.data)
            expected = {
                'error': 400,
                'error_type': 'BadData',
                'title': 'bad request',
                'text': response_json['text']
            }
            self.assertEqual(response_json, expected)
            self.assertEqual(response.status_code, 400)

    def test_all_zoos_head(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.head('/zoos/')
            self.assertEqual(response.data, b"")
            self.assertEqual(response.status_code, 200)

    def test_zoo_by_id_get(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.get('/zoos/1')
            response_json = json.loads(response.data)
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
                     'zoo_name': "a",
                     'zoo_id': 1},
                ],
            }
            self.assertEqual(expected, response_json)
            self.assertEqual(response.status_code, 200)

    def test_zoo_by_id_get_error(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.get('/zoos/100')
            response_json = json.loads(response.data)
            expected = {
                'error': 404,
                'error_type': 'BadId',
                'title': 'not found',
                'text': response_json['text']
            }
            self.assertEqual(response_json, expected)
            self.assertEqual(response.status_code, 404)

    def test_zoo_by_id_delete(self):
        with patch(self.session_patch_str, TestSession):
            all_zoos = json.loads(self.app.get('/zoos/').data)
            response = self.app.delete('/zoos/1')
            response_json = json.loads(response.data)
            del all_zoos[0]
            self.assertEqual(all_zoos, response_json)
            self.assertEqual(response.status_code, 200)

    def test_zoo_by_id_delete_bad_id(self):
        with patch(self.session_patch_str, TestSession):
            response = self.app.delete('/zoos/1000')
            response_json = json.loads(response.data)
            expected = {
                'error': 404,
                'error_type': 'BadId',
                'title': 'not found',
                'text': response_json['text']
            }
            self.assertEqual(response_json, expected)
            self.assertEqual(response.status_code, 404)


    # def test_zoo_by_id_put(self):
    #         with patch(self.session_patch_str, TestSession):
    #             json_data = {'a': 1, 'b': 'c'}
    #             self.app.put('/zoos/1', json=json_data)
    #
    #             self.handler_instance.put_zoo.assert_called_once_with('1', json_data)
    #             self.session_instance.close.assert_called_once()
    #
    # def test_zoo_by_id_head(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.head('/zoos/1')
    #
    #             self.handler_instance.get_zoo.assert_called_once_with('1')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_monkey_by_id_get(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.get('/monkeys/1')
    #
    #             self.handler_instance.get_monkey.assert_called_once_with('1')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_monkey_by_id_delete(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.delete('/monkeys/1')
    #
    #             self.handler_instance.delete_monkey.assert_called_once_with('1')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_monkey_by_id_put(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             json_data = {'a': 1, 'b': 'c'}
    #             self.app.put('/monkeys/1', json=json_data)
    #
    #             self.handler_instance.put_monkey.assert_called_once_with('1', json_data)
    #             self.session_instance.close.assert_called_once()
    #
    # def test_monkey_by_id_head(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.head('/monkeys/1')
    #
    #             self.handler_instance.get_monkey.assert_called_once_with('1')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_zoo_by_monkey_id_get(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.get('/monkeys/1/zoo')
    #
    #             self.handler_instance.get_zoo_by_monkey.assert_called_once_with('1')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_zoo_by_monkey_id_head(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.head('/monkeys/1/zoo')
    #
    #             self.handler_instance.get_zoo_by_monkey.assert_called_once_with('1')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_zoo_field_by_monkey_id_get(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.get('/monkeys/1/zoo/name')
    #
    #             self.handler_instance.get_zoo_field_by_monkey.assert_called_once_with('1', 'name')
    #             self.session_instance.close.assert_called_once()
    #
    # def test_zoo_field_by_monkey_id_head(self):
    #     with patch(self.handler_patch_str, self.handler_mock):
    #         with patch(self.session_patch_str, TestSession):
    #             self.app.head('/monkeys/1/zoo/name')
    #
    #             self.handler_instance.get_zoo_field_by_monkey.assert_called_once_with('1', 'name')
    #             self.session_instance.close.assert_called_once()
