import os
import csv
import mysql.connector as cnx

from zoo_server import USER, DATA_PATH, MONKEY_TABLE, ZOO_TABLE

TEST_DB = 'test'


def get_file_paths():
    zoo_file = os.path.join(DATA_PATH, 'zoo_data.txt')
    monkey_file = os.path.join(DATA_PATH, 'monkey_data.txt')
    return zoo_file, monkey_file


def load_csv(file_path):
    with open(file_path, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"', doublequote=True, skipinitialspace=True)
        raw = [row for row in csv_reader if row and not row[0].startswith('#')]
    return raw


class TestDataCreator(object):
    def __init__(self):
        self.db = cnx.connect(user=USER, host='localhost', database=TEST_DB)
        self.cur = self.db.cursor()
        self.zoo, self.monkey = get_file_paths()

    def drop_test_tables(self):
        self.cur.execute('drop table {};'.format(MONKEY_TABLE))
        self.cur.execute('drop table {};'.format(ZOO_TABLE))

    def execute_create_table_sql(self):
        parent_dir = os.path.dirname(os.path.dirname(DATA_PATH))
        sql_script = os.path.join(parent_dir, 'sql_scripts', 'create_tables.sql')
        with open(sql_script, 'r') as f:
            text = f.read()
            commands = text.split(';')

        for command in commands:
            if command.strip('\n'):
                self.cur.execute(command)

    def load_zoo(self):
        lines = load_csv(self.zoo)
        for line in lines:
            self.cur.execute("INSERT INTO {} (name, opens, closes) VALUES (%s, %s, %s)".format(ZOO_TABLE), line)
        self.db.commit()

    def load_monkey(self):
        self.cur.execute("SELECT name, id FROM {};".format(ZOO_TABLE))
        zoo_name_to_id = dict(self.cur.fetchall())

        lines = load_csv(self.monkey)

        converted = [_convert_line(line, zoo_name_to_id) for line in lines]

        for line in converted:
            command = "INSERT INTO {} (name, sex, flings_poop, poop_size, zoo_id) VALUES (%s, %s, %s, %s, %s)".format(
                MONKEY_TABLE)
            self.cur.execute(command, line)
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()


def _convert_line(line, zoo_id_conversions):
    out = []
    all_conversions = zoo_id_conversions.copy()
    all_conversions['TRUE'] = True
    all_conversions['FALSE'] = False
    for el in line:
        try:
            answer = int(el)
        except ValueError:
            answer = all_conversions.get(el, el)
        out.append(answer)
    return out


def main():
    creator = TestDataCreator()
    creator.drop_test_tables()
    creator.execute_create_table_sql()
    creator.load_zoo()
    creator.load_monkey()
    creator.close()


if __name__ == '__main__':
    main()
