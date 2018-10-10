import unittest
from unittest.mock import MagicMock, patch
from zoo_server import flask_app
from zoo_server.db_request_handler import DBRequestHandler
from zoo_server.data_base_session import DataBaseSession


class TestFlaskApp(unittest.TestCase):

    handler_patch_str = 'zoo_server.flask_app.DBRequestHandler'
    session_patch_str = 'zoo_server.data_base_session.DataBaseSession'

    methods = [key for key in DBRequestHandler.__dict__.keys() if not key.startswith('__')]

    def setUp(self):
        self.app = flask_app.app.test_client()
        flask_app.app.testing = True
        self.handler_mock = MagicMock(spec=DBRequestHandler)
        self.handler_instance = self.handler_mock.return_value

        self.session_mock = MagicMock(spec=DataBaseSession)
        self.session_instance = self.session_mock.return_value

        return_value = 'good', 200

        for method in self.methods:
            attr = getattr(self.handler_instance, method)
            attr.return_value = return_value

    def test_all_monkeys_get(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.get('/monkeys/')
                self.handler_instance.get_all_monkeys.assert_called_once()
                self.session_instance.close.assert_called_once()

    def test_all_monkeys_post(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                json_data = {'a': 1, 'b': 'hello'}
                self.app.post('/monkeys/', json=json_data)

                self.handler_instance.post_monkey.assert_called_once_with(json_data)
                self.session_instance.close.assert_called_once()

    def test_all_monkeys_head(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.head('/monkeys/')

                self.handler_instance.get_all_monkeys.assert_called_once()
                self.session_instance.close.assert_called_once()

    def test_all_zoos_get(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.get('/zoos/')

                self.handler_instance.get_all_zoos.assert_called_once()
                self.session_instance.close.assert_called_once()

    def test_all_zoos_post(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                json_data = {'a': 1, 'b':'hello'}
                self.app.post('/zoos/', json=json_data)

                self.handler_instance.post_zoo.assert_called_once_with(json_data)
                self.session_instance.close.assert_called_once()

    def test_all_zoos_head(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.head('/zoos/')

                self.handler_instance.get_all_zoos.assert_called_once()
                self.session_instance.close.assert_called_once()

    def test_zoo_by_id_get(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.get('/zoos/1')

                self.handler_instance.get_zoo.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_zoo_by_id_delete(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.delete('/zoos/1')

                self.handler_instance.delete_zoo.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_zoo_by_id_put(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                json_data = {'a': 1, 'b': 'c'}
                self.app.put('/zoos/1', json=json_data)

                self.handler_instance.put_zoo.assert_called_once_with('1', json_data)
                self.session_instance.close.assert_called_once()

    def test_zoo_by_id_head(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.head('/zoos/1')

                self.handler_instance.get_zoo.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_monkey_by_id_get(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.get('/monkeys/1')

                self.handler_instance.get_monkey.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_monkey_by_id_delete(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.delete('/monkeys/1')

                self.handler_instance.delete_monkey.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_monkey_by_id_put(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                json_data = {'a': 1, 'b': 'c'}
                self.app.put('/monkeys/1', json=json_data)

                self.handler_instance.put_monkey.assert_called_once_with('1', json_data)
                self.session_instance.close.assert_called_once()

    def test_monkey_by_id_head(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.head('/monkeys/1')

                self.handler_instance.get_monkey.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_zoo_by_monkey_id_get(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.get('/monkeys/1/zoo')

                self.handler_instance.get_zoo_by_monkey.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_zoo_by_monkey_id_head(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.head('/monkeys/1/zoo')

                self.handler_instance.get_zoo_by_monkey.assert_called_once_with('1')
                self.session_instance.close.assert_called_once()

    def test_zoo_field_by_monkey_id_get(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.get('/monkeys/1/zoo/name')

                self.handler_instance.get_zoo_field_by_monkey.assert_called_once_with('1', 'name')
                self.session_instance.close.assert_called_once()

    def test_zoo_field_by_monkey_id_head(self):
        with patch(self.handler_patch_str, self.handler_mock):
            with patch(self.session_patch_str, self.session_mock):
                self.app.head('/monkeys/1/zoo/name')

                self.handler_instance.get_zoo_field_by_monkey.assert_called_once_with('1', 'name')
                self.session_instance.close.assert_called_once()
