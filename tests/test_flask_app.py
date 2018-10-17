import unittest
from unittest.mock import patch

import json

from zoo_server import flask_app
from zoo_server.db_request_handler import DBRequestHandler, BadData, BadId


HANDLER_PATCH_STR = 'zoo_server.flask_app.DBRequestHandler'
SESSION_PATCH_STR = 'zoo_server.data_base_session.DataBaseSession'


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.app.test_client()
        flask_app.app.testing = True

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_monkeys_get(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_all_monkeys.return_value = 'ok', 200

        response = self.app.get('/monkeys/')
        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)

        handler_instance.get_all_monkeys.assert_called_once_with()

        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_monkeys_post(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.post_monkey.return_value = 'ok', 200

        json_data = {'a': 1}
        response = self.app.post('/monkeys/', json=json_data)
        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)

        handler_instance.post_monkey.assert_called_once_with(json_data)

        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_monkeys_post_bad_data(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        bad_data = {'ooop': 1}
        handler_instance.post_monkey.side_effect = BadData(json.dumps(bad_data))

        response = self.app.post('/monkeys/', json=bad_data)

        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadData',
            'title': 'bad request',
            'text': json.dumps(bad_data)
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.post_monkey.assert_called_once_with(bad_data)
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_monkeys_post_bad_json_str(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)

        response = self.app.post('/monkeys/', content_type="application/json", data='{"so bad":')

        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadRequest',
            'title': 'bad request',
            'text': response_json['text']
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        session_instance.close.assert_called_once_with()
        handler_instance.post_monkey.assert_not_called()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_monkeys_head(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_all_monkeys.return_value = 'good', 200

        response = self.app.head('/monkeys/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"")

        handler_instance.get_all_monkeys.assert_called_once_with()
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_zoos_get(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_all_zoos.return_value = 'good', 200

        response = self.app.get('/zoos/')
        self.assertEqual(response.data, b'good')
        self.assertEqual(response.status_code, 200)

        handler_instance.get_all_zoos.assert_called_once_with()
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_zoos_post(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.post_zoo.return_value = 'ok', 200
        json_data = {'a': 1}
        response = self.app.post('/zoos/', json=json_data)

        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)
        session_instance.close.assert_called_once_with()
        handler_instance.post_zoo.assert_called_once_with(json_data)

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_zoo_post_bad_data(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        bad_data = {'oops': 'a'}
        handler_instance.post_zoo.side_effect = BadData(json.dumps(bad_data))

        response = self.app.post('/zoos/', json=bad_data)
        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadData',
            'title': 'bad request',
            'text': json.dumps(bad_data)
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.post_zoo.assert_called_once_with(bad_data)
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_zoo_post_bad_json_string(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)

        response = self.app.post('/zoos/', content_type='application/json', data='{"ohono:')
        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadRequest',
            'title': 'bad request',
            'text': response_json['text']
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.post_zoo.assert_not_called()
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_all_zoos_head(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_all_zoos.return_value = 'ok', 200

        response = self.app.head('/zoos/')

        self.assertEqual(response.data, b"")
        self.assertEqual(response.status_code, 200)
        handler_instance.get_all_zoos.assert_called_once_with()
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_get(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_zoo.return_value = 'ok', 200

        response = self.app.get('/zoos/1')
        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)
        handler_instance.get_zoo.assert_called_once_with('1')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_get_error(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_zoo.side_effect = BadId('no')

        response = self.app.get('/zoos/100')
        response_json = json.loads(response.data)
        expected = {
            'error': 404,
            'error_type': 'BadId',
            'title': 'not found',
            'text': "no"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 404)
        handler_instance.get_zoo.assert_called_once_with('100')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_delete(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.delete_zoo.return_value = 'ok', 200
        response = self.app.delete('/zoos/1')
        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)
        handler_instance.delete_zoo.assert_called_once_with('1')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_delete_bad_id(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.delete_zoo.side_effect = BadId("nope")

        response = self.app.delete('/zoos/1000')
        response_json = json.loads(response.data)
        expected = {
            'error': 404,
            'error_type': 'BadId',
            'title': 'not found',
            'text': "nope"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 404)
        handler_instance.delete_zoo.assert_called_with('1000')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_put(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.put_zoo.return_value = 'ok', 200

        response = self.app.put('/zoos/1', json={'a': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok')
        handler_instance.put_zoo.assert_called_once_with('1', {'a': 1})
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_put_bad_id(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.put_zoo.side_effect = BadId('nope')

        response = self.app.put('/zoos/1', json={'a': 1})
        response_json = json.loads(response.data)
        expected = {
            'error': 404,
            'error_type': 'BadId',
            'title': 'not found',
            'text': "nope"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 404)
        handler_instance.put_zoo.assert_called_once_with('1', {'a': 1})
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_put_bad_data(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.put_zoo.side_effect = BadData('nope')

        response = self.app.put('/zoos/1', json={'a': 1})
        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadData',
            'title': 'bad request',
            'text': "nope"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.put_zoo.assert_called_once_with('1', {'a': 1})
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_bad_json(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)

        response = self.app.put('/zoos/1', content_type='application/json', data="{damnit: 1")
        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadRequest',
            'title': 'bad request',
            'text': response_json['text']
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.put_zoo.assert_not_called()
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_zoo_by_id_head(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_zoo.return_value = 'ok', 200

        response = self.app.head('/zoos/1')

        self.assertEqual(response.data, b"")
        self.assertEqual(response.status_code, 200)
        handler_instance.get_zoo.assert_called_once_with('1')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_get(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_monkey.return_value = 'ok', 200

        response = self.app.get('/monkeys/1')
        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)
        handler_instance.get_monkey.assert_called_once_with('1')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_get_error(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_monkey.side_effect = BadId('no')

        response = self.app.get('/monkeys/100')
        response_json = json.loads(response.data)
        expected = {
            'error': 404,
            'error_type': 'BadId',
            'title': 'not found',
            'text': "no"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 404)
        handler_instance.get_monkey.assert_called_once_with('100')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_delete(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.delete_monkey.return_value = 'ok', 200
        response = self.app.delete('/monkeys/1')
        self.assertEqual(response.data, b'ok')
        self.assertEqual(response.status_code, 200)
        handler_instance.delete_monkey.assert_called_once_with('1')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_delete_bad_id(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.delete_monkey.side_effect = BadId("nope")

        response = self.app.delete('/monkeys/1000')
        response_json = json.loads(response.data)
        expected = {
            'error': 404,
            'error_type': 'BadId',
            'title': 'not found',
            'text': "nope"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 404)
        handler_instance.delete_monkey.assert_called_with('1000')
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_put(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.put_monkey.return_value = 'ok', 200

        response = self.app.put('/monkeys/1', json={'a': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok')
        handler_instance.put_monkey.assert_called_once_with('1', {'a': 1})
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_put_bad_id(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.put_monkey.side_effect = BadId('nope')

        response = self.app.put('/monkeys/1', json={'a': 1})
        response_json = json.loads(response.data)
        expected = {
            'error': 404,
            'error_type': 'BadId',
            'title': 'not found',
            'text': "nope"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 404)
        handler_instance.put_monkey.assert_called_once_with('1', {'a': 1})
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_put_bad_data(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.put_monkey.side_effect = BadData('nope')

        response = self.app.put('/monkeys/1', json={'a': 1})
        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadData',
            'title': 'bad request',
            'text': "nope"
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.put_monkey.assert_called_once_with('1', {'a': 1})
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_bad_json(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)

        response = self.app.put('/monkeys/1', content_type='application/json', data="{damnit: 1")
        response_json = json.loads(response.data)
        expected = {
            'error': 400,
            'error_type': 'BadRequest',
            'title': 'bad request',
            'text': response_json['text']
        }
        self.assertEqual(response_json, expected)
        self.assertEqual(response.status_code, 400)
        handler_instance.put_monkey.assert_not_called()
        session_instance.close.assert_called_once_with()

    @patch(SESSION_PATCH_STR)
    @patch(HANDLER_PATCH_STR)
    def test_monkey_by_id_head(self, handler_class, session_class):
        handler_instance, session_instance = create_instances(handler_class, session_class)
        handler_instance.get_monkey.return_value = 'ok', 200

        response = self.app.head('/monkeys/1')

        self.assertEqual(response.data, b"")
        self.assertEqual(response.status_code, 200)
        handler_instance.get_monkey.assert_called_once_with('1')
        session_instance.close.assert_called_once_with()


def create_instances(handler_class_mock, session_class_mock):
    handler_instance = handler_class_mock.return_value
    session_instance = session_class_mock.return_value
    handler_instance.mock_add_spec(DBRequestHandler)
    return handler_instance, session_instance
