import os
import csv
import mysql.connector as cnx


def get_file_paths():
    parent_dir = os.path.dirname(__file__)
    data_dir = os.path.join(parent_dir, 'zoo_server', 'data')
    zoo_file = os.path.join(data_dir, 'zoo_data.txt')
    monkey_file = os.path.join(data_dir, 'monkey_data.txt')
    return zoo_file, monkey_file


def load_csv(file_path):
    with open(file_path, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"', doublequote=True, skipinitialspace=True)
        raw = [row for row in csv_reader if row and not row[0].startswith('#')]
    return raw


class TestLoader(object):
    def __init__(self):
        self.db = cnx.connect(user='zoo_guest', host='localhost', database='zoo')
        self.cur = self.db.cursor()
        self.zoo, self.monkey = get_file_paths()

    def load_zoo(self):
        lines = load_csv(self.zoo)
        for line in lines:
            self.cur.execute("INSERT INTO zoo (name, opens, closes) VALUES (%s, %s, %s)", line)
        self.db.commit()

    def load_monkey(self):
        self.cur.execute("SELECT name, id FROM zoo;")
        zoo_name_to_id = dict(self.cur.fetchall())

        lines = load_csv(self.monkey)

        converted = [_convert_line(line, zoo_name_to_id) for line in lines]

        for line in converted:
            command = "INSERT INTO monkey (name, sex, flings_poop, poop_size, zoo_id) VALUES (%s, %s, %s, %s, %s)"
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


if __name__ == '__main__':
    x = TestLoader()
    x.load_zoo()
    x.load_monkey()
    x.close()
