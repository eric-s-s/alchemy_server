import unittest
from unittest.mock import MagicMock, patch
from zoo_server import flask_app
from zoo_server.request_handler import RequestHandler


class TestFlaskApp(unittest.TestCase):

    patch_str = 'zoo_server.request_handler.RequestHandler'

    methods = [key for key in RequestHandler.__dict__.keys() if not key.startswith('__')]

    def setUp(self):
        self.app = flask_app.app.test_client()
        flask_app.app.testing = True
        self.mock = MagicMock(spec=RequestHandler)
        self.instance = self.mock.return_value

        return_value = 'good', 200

        for method in self.methods:
            attr = getattr(self.instance, method)
            attr.return_value = return_value

    def test_all_monkeys_get(self):
        with patch(self.patch_str, self.mock):
            self.app.get('/monkeys/')

            self.instance.get_all_monkeys.assert_called_once()
            self.instance.close_connection.assert_called_once()

    def test_all_monkeys_delete(self):
        with patch(self.patch_str, self.mock):
            self.app.delete('/monkeys/')

            self.instance.delete_all_monkeys.assert_called_once()
            self.instance.close_connection.assert_called_once()

    def test_all_monkeys_post(self):
        with patch(self.patch_str, self.mock):
            json_data = {'a': 1, 'b': 'hello'}
            self.app.post('/monkeys/', json=json_data)

            self.instance.post_monkey.assert_called_once_with(json_data)
            self.instance.close_connection.assert_called_once()

    def test_all_monkeys_head(self):
        with patch(self.patch_str, self.mock):
            self.app.head('/monkeys/')

            self.instance.get_all_monkeys.assert_called_once()
            self.instance.close_connection.assert_called_once()

    def test_all_zoos_get(self):
        with patch(self.patch_str, self.mock):
            self.app.get('/zoos/')

            self.instance.get_all_zoos.assert_called_once()
            self.instance.close_connection.assert_called_once()

    def test_all_zoos_delete(self):
        with patch(self.patch_str, self.mock):
            self.app.delete('/zoos/')

            self.instance.delete_all_zoos.assert_called_once()
            self.instance.close_connection.assert_called_once()

    def test_all_zoos_post(self):
        with patch(self.patch_str, self.mock):
            json_data = {'a': 1, 'b':'hello'}
            self.app.post('/zoos/', json=json_data)

            self.instance.post_zoo.assert_called_once_with(json_data)
            self.instance.close_connection.assert_called_once()

    def test_all_zoos_head(self):
        with patch(self.patch_str, self.mock):
            self.app.head('/zoos/')

            self.instance.get_all_zoos.assert_called_once()
            self.instance.close_connection.assert_called_once()

    def test_zoo_by_name_get(self):
        with patch(self.patch_str, self.mock):
            self.app.get('/zoos/a')

            self.instance.get_single_zoo.assert_called_once_with('a')
            self.instance.close_connection.assert_called_once()

    def test_zoo_by_name_delete(self):
        with patch(self.patch_str, self.mock):
            self.app.delete('/zoos/a')

            self.instance.delete_single_zoo.assert_called_once_with('a')
            self.instance.close_connection.assert_called_once()

    def test_zoo_by_name_put(self):
        with patch(self.patch_str, self.mock):
            json_data = {'a': 1, 'b': 'c'}
            self.app.put('/zoos/a', json=json_data)

            self.instance.put_zoo.assert_called_once_with('a', json_data)
            self.instance.close_connection.assert_called_once()

    def test_zoo_by_name_head(self):
        with patch(self.patch_str, self.mock):
            self.app.head('/zoos/a')

            self.instance.get_single_zoo.assert_called_once_with('a')
            self.instance.close_connection.assert_called_once()

    def test_monkey_by_id_get(self):
        with patch(self.patch_str, self.mock):
            self.app.get('/monkeys/1')

            self.instance.get_single_monkey.assert_called_once_with('1')
            self.instance.close_connection.assert_called_once()

    def test_monkey_by_id_delete(self):
        with patch(self.patch_str, self.mock):
            self.app.delete('/monkeys/1')

            self.instance.delete_single_monkey.assert_called_once_with('1')
            self.instance.close_connection.assert_called_once()

    def test_monkey_by_id_put(self):
        with patch(self.patch_str, self.mock):
            json_data = {'a': 1, 'b': 'c'}
            self.app.put('/monkeys/1', json=json_data)

            self.instance.put_monkey.assert_called_once_with('1', json_data)
            self.instance.close_connection.assert_called_once()

    def test_monkey_by_id_head(self):
        with patch(self.patch_str, self.mock):
            self.app.head('/monkeys/1')

            self.instance.get_single_monkey.assert_called_once_with('1')
            self.instance.close_connection.assert_called_once()

    def test_zoo_by_monkey_id_get(self):
        with patch(self.patch_str, self.mock):
            self.app.get('/monkeys/1/zoo')

            self.instance.get_zoo_by_monkey.assert_called_once_with('1')
            self.instance.close_connection.assert_called_once()

    def test_zoo_by_monkey_id_head(self):
        with patch(self.patch_str, self.mock):
            self.app.head('/monkeys/1/zoo')

            self.instance.get_zoo_by_monkey.assert_called_once_with('1')
            self.instance.close_connection.assert_called_once()

    def test_zoo_field_by_monkey_id_get(self):
        with patch(self.patch_str, self.mock):
            self.app.get('/monkeys/1/zoo/name')

            self.instance.get_zoo_field_by_monkey.assert_called_once_with('1', 'name')
            self.instance.close_connection.assert_called_once()

    def test_zoo_field_by_monkey_id_head(self):
        with patch(self.patch_str, self.mock):
            self.app.head('/monkeys/1/zoo/name')

            self.instance.get_zoo_field_by_monkey.assert_called_once_with('1', 'name')
            self.instance.close_connection.assert_called_once()
