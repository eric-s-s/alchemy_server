from datetime import time
import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as BaseSession

from tests import TEST_DATA
from zoo_server.db_classes import Base, Monkey, Zoo

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)


# def get_file_paths():
#     zoo_file = os.path.join(DATA_PATH, 'zoo_data.txt')
#     monkey_file = os.path.join(DATA_PATH, 'monkey_data.txt')
#     return zoo_file, monkey_file


def load_csv(file_path):
    with open(file_path, 'r', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"', doublequote=True, skipinitialspace=True)
        raw = [row for row in csv_reader if row and not row[0].startswith('#')]
    return raw


def load_zoo(session):
    zoo_path = os.path.join(TEST_DATA, 'test_zoo.txt')
    lines = load_csv(zoo_path)
    keys = ['name', 'opens', 'closes']
    for line in lines:
        kwargs = dict(zip(keys, line))
        new_kwargs = {key: value if key == 'name' else _parse_time_str(value) for key, value in kwargs.items()}
        zoo = Zoo(**new_kwargs)
        session.add(zoo)
    session.commit()


def load_monkey(session: BaseSession):
    monkey_path = os.path.join(TEST_DATA, 'test_monkey.txt')
    lines = load_csv(monkey_path)
    keys = ['name', 'sex', 'flings_poop', 'poop_size', 'zoo_name']
    for line in lines:
        raw_data = dict(zip(keys, line))
        new_data = raw_data.copy()
        del new_data['zoo_name']
        zoo_id = session.query(Zoo.id).filter(Zoo.name == raw_data['zoo_name']).first()[0]
        new_data['zoo_id'] = zoo_id

        new_data['flings_poop'] = True if raw_data['flings_poop'].lower() == 'true' else False
        new_monkey = Monkey(**new_data)
        session.add(new_monkey)
    session.commit()


def _parse_time_str(time_str):
    hour, minute = time_str.split(':')
    return time(int(hour), int(minute))


def create_all_test_data(session: BaseSession):
    Base.metadata.create_all(engine)

    for zoo in session.query(Zoo).all():
        session.delete(zoo)
    session.commit()
    load_zoo(session)
    load_monkey(session)


if __name__ == '__main__':
    new_session = Session()
    create_all_test_data(new_session)
    all_zoos = new_session.query(Zoo).all()

    from pprint import pprint
    pprint([zoo.to_dict() for zoo in all_zoos])
    new_session.close()
