from datetime import time
import json
from contextlib import contextmanager

from alchemy_server.db_classes import Monkey, Zoo, safe_session, Session


# with safe_session() as session:
#
#     print(session.query(Monkey).all())
#     print(session.query(Zoo).all())
#     the_zoo = session.query(Zoo).filter(Zoo.name == "Wacky Zachy's Monkey Attacky").first()
#     print(the_zoo.to_dict())
#     print(the_zoo.monkeys)


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

        keys = ['opens', 'closes']
        bad_fields = [key for key in json_data.keys() if key not in keys]
        if bad_fields:
            return "following json fields not allowed: {}".format(bad_fields), 400
        for key, raw_value in json_data.items():
            value = _parse_time_str(raw_value)
            setattr(zoo, key, value)
        self.session.commit()
        return json.dumps(zoo.to_dict()), 200
#             value = _convert_value(raw_value)
#             params = {'zoo': ZOO_TABLE, 'key': key}
#             cmd = "UPDATE {zoo} SET {key} = %s WHERE name = %s".format(**params)
#             self.cur.execute(cmd, (value, zoo_name))
#         self.db.commit()
#         return self.get_single_zoo(zoo_name)
#
    def put_monkey(self, monkey_id, json_data):
        """
        json fields: name, sex, flings_poop, poop_size, zoo_name
        """
        pass
#         keys = ['name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
#         bad_fields = [key for key in json_data.keys() if key not in keys]
#         if bad_fields:
#             print('\n\n\nNNNOOOOO\n\n\n')
#             return "following json fields not allowed: {}".format(bad_fields), 400
#         for key, raw_value in json_data.items():
#             value = _convert_value(raw_value)
#             params = {'monkey': MONKEY_TABLE, 'key': key}
#             if key == 'zoo_name':
#                 params['zoo'] = ZOO_TABLE
#                 cmd = ("UPDATE {monkey}"
#                        " SET zoo_id = (SELECT id FROM {zoo} WHERE {zoo}.name = %s)"
#                        " WHERE id = %s"
#                        ).format(**params)
#             else:
#                 cmd = "UPDATE {monkey} SET {key} = %s WHERE id = %s".format(**params)
#             self.cur.execute(cmd, (value, monkey_id))
#         self.db.commit()
#         return self.get_single_monkey(monkey_id)
#
    def post_zoo(self, json_data):
        """
        json fields: name, opens, closes
        """
        pass
#         keys = ['name', 'opens', 'closes']
#         values = [_convert_value(json_data[key]) for key in keys]
#
#         cmd = "INSERT INTO {zoo} (name, opens, closes) VALUES (%s, %s, %s)".format(zoo=ZOO_TABLE)
#         self.cur.execute(cmd, values)
#         self.db.commit()
#
#         return self.get_single_zoo(json_data['name'])
#
    def post_monkey(self, json_data):
        """
        json fields: name, sex, flings_poop, poop_size, zoo_name
        """
        pass
#         keys = ['name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
#         values = [_convert_value(json_data[key]) for key in keys]
#         cmd = (
#             "INSERT INTO {monkey} (name, sex, flings_poop, poop_size, zoo_id)"
#             " VALUES (%s, %s, %s, %s, (SELECT id FROM {zoo} WHERE zoo.name = %s))"
#         ).format(zoo=ZOO_TABLE, monkey=MONKEY_TABLE)
#         self.cur.execute(cmd, values)
#         self.db.commit()
#
#         self.cur.execute("SELECT MAX(id) FROM {monkey} ".format(monkey=MONKEY_TABLE))
#         monkey_id = self.cur.fetchone()[0]
#         return self.get_single_monkey(monkey_id)
#
    def delete_all_zoos(self):
        pass
#         self.cur.execute("DELETE FROM {}".format(ZOO_TABLE))
#         self.db.commit()
#         return self.get_all_zoos()
#
    def delete_all_monkeys(self):
        pass
#         self.cur.execute("DELETE FROM {}".format(MONKEY_TABLE))
#         self.db.commit()
#         return self.get_all_monkeys()
#
    def delete_single_monkey(self, monkey_id):
        pass
#         self.cur.execute("DELETE FROM {} WHERE id = %s".format(MONKEY_TABLE), (monkey_id,))
#         self.db.commit()
#         return self.get_all_monkeys()
#
    def delete_single_zoo(self, zoo_name):
        pass
#         self.cur.execute("DELETE FROM {} WHERE name = %s".format(ZOO_TABLE), (zoo_name,))
#         self.db.commit()
#         return self.get_all_zoos()
#
    def close_connection(self):
        self.session.close()

#     def _get_fields(self, table):
#         self.cur.execute("show columns from {};".format(table))
#         return [field[0] for field in self.cur.fetchall()]
#
#     def _get_all(self, table):
#         fields = self._get_fields(table)
#         self.cur.execute("select * from {};".format(table))
#         answers = self.cur.fetchall()
#         return [{field: entry[index] for index, field in enumerate(fields)} for entry in answers]
#
#
# def _create_dict(keys, values):
#     items = zip(keys, values)
#     return {key: str(value) if isinstance(value, timedelta) else value for key, value in items}
#
#
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
    hour, min = time_str.split(':')
    return time(int(hour), int(min))


@contextmanager
def safe_handler():
    handler = RequestHandler()
    try:
        yield handler
    finally:
        handler.close_connection()