from zoo_server import USER, DB

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session(host='localhost'):
    engine = create_engine("mysql://{}@{}/{}".format(USER, host, DB),
                           encoding='latin1')

    return sessionmaker(bind=engine)()

