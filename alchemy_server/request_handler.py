import json
from datetime import timedelta

import mysql.connector as cnx

from alchemy_server import ZOO_TABLE, MONKEY_TABLE, USER, DB


class RequestHandler(object):
    def __init__(self):
        self.db = cnx.connect(
                host='localhost',
                user=USER,
                database=DB    
            )
        self.cur = self.db.cursor(buffered=True)

    def get_all_zoos(self):
        """
        return fields: name, opens, closes, number_of_monkeys

        :return: json_str, code
        """
        cmd = (
            "SELECT"
            "   {zoo}.name,"
            "   {zoo}.opens,"
            "   {zoo}.closes, "
            "   CASE WHEN monkey_count IS NULL THEN 0 ELSE monkey_count END AS monkey_count"
            " FROM zoo LEFT JOIN ("
            "   SELECT zoo_id, COUNT(*) AS monkey_count"
            "   FROM {monkey} "
            "   GROUP BY zoo_id"
            ") AS tmp ON {zoo}.id = tmp.zoo_id"
        ).format(zoo=ZOO_TABLE, monkey=MONKEY_TABLE)
        self.cur.execute(cmd)
        raw_answer = self.cur.fetchall()

        keys = ['name', 'opens', 'closes', 'number_of_monkeys']
        answer = [_create_dict(keys, values) for values in raw_answer]
        return json.dumps(answer), 200

    def get_all_monkeys(self):
        """
        return fields: id, name, sex, flings_poop, poop_size, zoo_name

        :return: json_str, response_code
        """
        cmd = (
            "SELECT {monkey}.id, {monkey}.name, sex, "
            "   CASE WHEN flings_poop=TRUE THEN \"TRUE\" ELSE \"FALSE\" END,"
            "   poop_size, {zoo}.name"
            " FROM {monkey} INNER JOIN {zoo} ON {monkey}.zoo_id = {zoo}.id"
        ).format(monkey=MONKEY_TABLE, zoo=ZOO_TABLE)
        self.cur.execute(cmd)
        raw_answer = self.cur.fetchall()
        keys = ['id', 'name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
        answer = [_create_dict(keys, values) for values in raw_answer]
        return json.dumps(answer), 200

    def get_single_zoo(self, zoo_name):
        """
        return fields: name, opens, closes, monkey_ids

        :return: json_str, response_code
        """
        self.cur.execute("SELECT id FROM {zoo} WHERE name=%s".format(zoo=ZOO_TABLE), (zoo_name,))
        answer = self.cur.fetchone()
        if answer is None:
            return "name does not exist: {}".format(zoo_name), 404
        zoo_id = answer[0]

        self.cur.execute("SELECT id FROM {} WHERE zoo_id=%s".format(MONKEY_TABLE), (zoo_id,))
        monkey_ids = [el[0] for el in self.cur.fetchall()]

        self.cur.execute("SELECT name, opens, closes FROM zoo WHERE id=%s", (zoo_id,))
        answer = _create_dict(['name', 'opens', 'closes'], self.cur.fetchone())
        answer['monkey_ids'] =monkey_ids
        return json.dumps(answer), 200

    def get_single_monkey(self, monkey_id):
        """
        return fields: id, name, sex, flings_poop, poop_size, zoo_name

        :return: json_str, response_code
        """
        cmd = (
            "SELECT {monkey}.id, {monkey}.name, {monkey}.sex, "
            "       CASE WHEN {monkey}.flings_poop=TRUE THEN \"TRUE\" ELSE \"FALSE\" END, "
            "       {monkey}.poop_size, {zoo}.name"
            " FROM {monkey} INNER JOIN {zoo} ON {monkey}.zoo_id = {zoo}.id"
            " WHERE {monkey}.id = %s"
        ).format(monkey=MONKEY_TABLE, zoo=ZOO_TABLE)
        self.cur.execute(cmd, (monkey_id,))
        answer = self.cur.fetchone()
        if answer is None:
            return "monkey_id does not exist: {}".format(monkey_id), 404
        answer_dict = _create_dict(['id', 'name', 'sex', 'flings_poop', 'poop_size', 'zoo_name'], answer)
        return json.dumps(answer_dict), 200

    def get_zoo_by_monkey(self, monkey_id):
        cmd = "SELECT {zoo}.name FROM {zoo} JOIN {monkey} ON {zoo}.id = {monkey}.zoo_id WHERE {monkey}.id = %s"
        cmd = cmd.format(zoo=ZOO_TABLE, monkey=MONKEY_TABLE)
        self.cur.execute(cmd, (monkey_id,))
        answer = self.cur.fetchone()
        if answer is None:
            return "monkey_id does not exists: {}".format(monkey_id), 404
        zoo_name = answer[0]
        return self.get_single_zoo(zoo_name)

    def put_zoo(self, zoo_name, json_data):
        """
        json fields: opens, closes
        """
        keys = ['opens', 'closes']
        bad_fields = [key for key in json_data.keys() if key not in keys]
        if bad_fields:
            return "following json fields not allowed: {}".format(bad_fields), 400
        for key, raw_value in json_data.items():
            value = _convert_value(raw_value)
            params = {'zoo': ZOO_TABLE, 'key': key}
            cmd = "UPDATE {zoo} SET {key} = %s WHERE name = %s".format(**params)
            self.cur.execute(cmd, (value, zoo_name))
        self.db.commit()
        return self.get_single_zoo(zoo_name)

    def put_monkey(self, monkey_id, json_data):
        """
        json fields: name, sex, flings_poop, poop_size, zoo_name
        """
        keys = ['name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
        bad_fields = [key for key in json_data.keys() if key not in keys]
        if bad_fields:
            print('\n\n\nNNNOOOOO\n\n\n')
            return "following json fields not allowed: {}".format(bad_fields), 400
        for key, raw_value in json_data.items():
            value = _convert_value(raw_value)
            params = {'monkey': MONKEY_TABLE, 'key': key}
            if key == 'zoo_name':
                params['zoo'] = ZOO_TABLE
                cmd = ("UPDATE {monkey}"
                       " SET zoo_id = (SELECT id FROM {zoo} WHERE {zoo}.name = %s)"
                       " WHERE id = %s"
                       ).format(**params)
            else:
                cmd = "UPDATE {monkey} SET {key} = %s WHERE id = %s".format(**params)
            self.cur.execute(cmd, (value, monkey_id))
        self.db.commit()
        return self.get_single_monkey(monkey_id)

    def post_zoo(self, json_data):
        """
        json fields: name, opens, closes
        """
        keys = ['name', 'opens', 'closes']
        values = [_convert_value(json_data[key]) for key in keys]

        cmd = "INSERT INTO {zoo} (name, opens, closes) VALUES (%s, %s, %s)".format(zoo=ZOO_TABLE)
        self.cur.execute(cmd, values)
        self.db.commit()

        return self.get_single_zoo(json_data['name'])

    def post_monkey(self, json_data):
        """
        json fields: name, sex, flings_poop, poop_size, zoo_name
        """
        keys = ['name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
        values = [_convert_value(json_data[key]) for key in keys]
        cmd = (
            "INSERT INTO {monkey} (name, sex, flings_poop, poop_size, zoo_id)"
            " VALUES (%s, %s, %s, %s, (SELECT id FROM {zoo} WHERE zoo.name = %s))"
        ).format(zoo=ZOO_TABLE, monkey=MONKEY_TABLE)
        self.cur.execute(cmd, values)
        self.db.commit()

        self.cur.execute("SELECT MAX(id) FROM {monkey} ".format(monkey=MONKEY_TABLE))
        monkey_id = self.cur.fetchone()[0]
        return self.get_single_monkey(monkey_id)

    def delete_all_zoos(self):
        self.cur.execute("DELETE FROM {}".format(ZOO_TABLE))
        self.db.commit()
        return self.get_all_zoos()

    def delete_all_monkeys(self):
        self.cur.execute("DELETE FROM {}".format(MONKEY_TABLE))
        self.db.commit()
        return self.get_all_monkeys()

    def delete_single_monkey(self, monkey_id):
        self.cur.execute("DELETE FROM {} WHERE id = %s".format(MONKEY_TABLE), (monkey_id,))
        self.db.commit()
        return self.get_all_monkeys()

    def delete_single_zoo(self, zoo_name):
        self.cur.execute("DELETE FROM {} WHERE name = %s".format(ZOO_TABLE), (zoo_name,))
        self.db.commit()
        return self.get_all_zoos()

    def close_connection(self):
        self.db.commit()
        self.db.close()

    def _get_fields(self, table):
        self.cur.execute("show columns from {};".format(table))
        return [field[0] for field in self.cur.fetchall()]

    def _get_all(self, table):
        fields = self._get_fields(table)
        self.cur.execute("select * from {};".format(table))
        answers = self.cur.fetchall()
        return [{field: entry[index] for index, field in enumerate(fields)} for entry in answers]


def _create_dict(keys, values):
    items = zip(keys, values)
    return {key: str(value) if isinstance(value, timedelta) else value for key, value in items}


def _convert_value(value):
    if not isinstance(value, str):
        return value
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return value



if __name__ == '__main__':
    from pprint import pprint
    x = RequestHandler()
        
    print(x._get_fields('zoo'))
    pprint(x._get_all('monkey'))
