import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///oab.db')
Base = declarative_base()

class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(Integer, ForeignKey('state.id'))

class NameType(enum.Enum):
    Unknown = 0
    Forename = 1
    Surname = 2

class Name(Base):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Enum(NameType))

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    number = Column(Integer)
    city = Column(Integer, ForeignKey('city.id'))

class HasName(Base):
    __tablename__ = 'has_name'
    id = Column(Integer, primary_key=True)
    person = Column(Integer, ForeignKey('person.id'))
    name = Column(Integer, ForeignKey('name.id'))
    position = Column(Integer)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
