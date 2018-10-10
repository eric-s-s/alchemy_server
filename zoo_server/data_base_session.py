"""
NOTE: DataBaseSession requires binding to an engine using DataBaseSession.configure(bind=some_engine)
"""


from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

DataBaseSession = sessionmaker()


@contextmanager
def data_base_session_scope():
    session = DataBaseSession()
    try:
        yield session
    finally:
        session.close()
