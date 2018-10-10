import enum

from zoo_server import ZOO_TABLE, MONKEY_TABLE


from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Sex(enum.Enum):
    m = 'male'
    f = 'female'


class Zoo(Base):
    __tablename__ = ZOO_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    opens = Column(Time, nullable=False)
    closes = Column(Time, nullable=False)

    monkeys = relationship('Monkey', back_populates='zoo',
                           cascade='delete')

    def to_dict(self):
        format_str = '%H:%M'
        monkeys = [monkey.to_dict() for monkey in self.monkeys]
        return {
            'id': self.id,
            'name': self.name,
            'opens': self.opens.strftime(format_str),
            'closes': self.closes.strftime(format_str),
            'monkeys': monkeys
        }


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
            'zoo_name': self.zoo.name,
            'zoo_id': self.zoo_id
        }
