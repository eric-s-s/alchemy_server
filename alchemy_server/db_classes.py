from contextlib import contextmanager
import enum

from alchemy_server import ZOO_TABLE, MONKEY_TABLE, USER, DB


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Boolean, UniqueConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql://{}@localhost/{}".format(USER, DB),
                       encoding='latin1')


Session = sessionmaker(bind=engine)


Base = declarative_base()


class Sex(enum.Enum):
    m = 'male'
    f = 'female'


class Zoo(Base):
    __tablename__ = ZOO_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    opens = Column(Time, nullable=False)
    closes = Column(Time, nullable=False)

    monkeys = relationship('Monkey', back_populates='zoo',
                           cascade='delete')

    def to_dict(self):
        format_str = '%H:%M'
        monkeys = [monkey.to_dict() for monkey in self.monkeys]
        return {
            'name': self.name,
            'opens': self.opens.strftime(format_str),
            'closes': self.closes.strftime(format_str),
            'monkeys': monkeys
        }

    def __repr__(self):
        return "<Zoo {!r}, {!r}. {!r}>".format(self.name, self.opens, self.closes)


class Monkey(Base):
    __tablename__ = MONKEY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    flings_poop = Column(Boolean, nullable=False)
    poop_size = Column(Integer, nullable=False)
    zoo_id = Column(Integer, ForeignKey('zoo.id'), nullable=False)

    zoo = relationship('Zoo', back_populates='monkeys')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sex': self.sex.name,
            'flings_poop': str(self.flings_poop).upper(),
            'poop_size': self.poop_size,
            'zoo_name': self.zoo.name
        }

    def __repr__(self):
        out = "<monkey: " + 6 * "{!r}, "
        out = out.rstrip(', ') + '>'
        return out.format(self.id, self.name, self.sex, self.flings_poop, self.poop_size, self.zoo.name)


@contextmanager
def safe_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

