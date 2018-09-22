from datetime import time
import json
from contextlib import contextmanager

from alchemy_server.db_classes import Monkey, Zoo, Session


class RequestHandler(object):
    def __init__(self):
        self.session = Session()

    def get_all_zoos(self):
        """
        return fields: name, opens, closes, number_of_monkeys

        :return: json_str, code
        """
        zoos = self.session.query(Zoo).all()
        answer = [zoo.to_dict() for zoo in zoos]
        return json.dumps(answer), 200

    def get_all_monkeys(self):
        """
        return fields: id, name, sex, flings_poop, poop_size, zoo_name

        :return: json_str, response_code
        """
        monkeys = self.session.query(Monkey).all()
        answer = [monkey.to_dict() for monkey in monkeys]
        return json.dumps(answer), 200

    def get_single_zoo(self, zoo_name):
        """
        return fields: name, opens, closes, monkey_ids

        :return: json_str, response_code
        """
        zoo = self.session.query(Zoo).filter(Zoo.name == zoo_name).first()
        if zoo is None:
            return "zoo name does not exist: {}".format(zoo_name), 404
        return json.dumps(zoo.to_dict()), 200

    def get_single_monkey(self, monkey_id):
        """
        return fields: id, name, sex, flings_poop, poop_size, zoo_name

        :return: json_str, response_code
        """
        monkey = self.session.query(Monkey).filter(Monkey.id == monkey_id).first()
        if monkey is None:
            return "monkey id does not exists: {}".format(monkey_id), 404
        return json.dumps(monkey.to_dict()), 200

    def get_zoo_by_monkey(self, monkey_id):
        monkey = self.session.query(Monkey).filter(Monkey.id == monkey_id).first()
        if monkey is None:
            return "monkey id does not exists: {}".format(monkey_id)
        return json.dumps(monkey.zoo.to_dict()), 200

    def put_zoo(self, zoo_name, json_data):
        """
        json fields: opens, closes
        """
        zoo = self.session.query(Zoo).filter(Zoo.name == zoo_name).first()
        if zoo is None:
            return "zoo_name does not exists: {}".format(zoo_name), 404
        keys = ['opens', 'closes']
        bad_fields = [key for key in json_data.keys() if key not in keys]
        if bad_fields:
            return "following json fields not allowed: {}".format(bad_fields), 400
        for key, raw_value in json_data.items():
            value = _parse_time_str(raw_value)
            setattr(zoo, key, value)
        self.session.commit()
        return json.dumps(zoo.to_dict()), 200

    def put_monkey(self, monkey_id, json_data):
        """
        json fields: name, sex, flings_poop, poop_size, zoo_name
        """
        monkey = self.session.query(Monkey).filter(Monkey.id == monkey_id).first()
        keys = ['name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
        bad_fields = [key for key in json_data.keys() if key not in keys]
        if bad_fields:
            return "following json fields not allowed: {}".format(bad_fields), 400
        for key, raw_value in json_data.items():
            value = _convert_value(raw_value)
            if key == 'zoo_name':
                zoo_id = self.session.query(Zoo.id).filter(Zoo.name == value).first()
                setattr(monkey, 'zoo_id', zoo_id)
            else:
                setattr(monkey, key, value)
        self.session.commit()
        return json.dumps(monkey.to_dict()), 200

    def post_zoo(self, json_data):
        """
        json fields: name, opens, closes
        """
        new_data = json_data.copy()
        for key in ['opens', 'closes']:
            new_data[key] = _parse_time_str(json_data[key])
        new_zoo = Zoo(**new_data)
        self.session.add(new_zoo)
        self.session.commit()
        return json.dumps(new_zoo.to_dict()), 200

    def post_monkey(self, json_data):
        """
        json fields: name, sex, flings_poop, poop_size, zoo_name
        """
        new_data = json_data.copy()
        new_data['flings_poop'] = True if json_data['flings_poop'].lower() == 'true' else False
        new_data['zoo_id'] = self.session.query(Zoo.id).filter(Zoo.name == json_data['zoo_name']).first()
        del new_data['zoo_name']
        new_monkey = Monkey(**new_data)
        self.session.add(new_monkey)
        self.session.commit()
        return json.dumps(new_monkey.to_dict()), 200

    def delete_all_zoos(self):
        for zoo in self.session.query(Zoo).all():
            self.session.delete(zoo)
        self.session.commit()
        return self.get_all_zoos()

    def delete_all_monkeys(self):
        for monkey in self.session.query(Monkey).all():
            self.session.delete(monkey)
        self.session.commit()
        return self.get_all_monkeys()

    def delete_single_monkey(self, monkey_id):
        monkey = self.session.query(Monkey).filter(Monkey.id == monkey_id).first()
        self.session.delete(monkey)
        self.session.commit()
        return self.get_all_monkeys()

    def delete_single_zoo(self, zoo_name):
        zoo = self.session.query(Zoo).filter(Zoo.name == zoo_name).first()
        self.session.delete(zoo)
        self.session.commit()
        return self.get_all_zoos()

    def close_connection(self):
        self.session.close()


def _convert_value(value):
    if not isinstance(value, str):
        return value
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return value


def _parse_time_str(time_str):
    hour, minute = time_str.split(':')
    return time(int(hour), int(minute))


@contextmanager
def safe_handler():
    handler = RequestHandler()
    try:
        yield handler
    finally:
        handler.close_connection()
