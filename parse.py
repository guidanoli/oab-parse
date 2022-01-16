from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

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

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mat = Column(Integer)
    city = Column(Integer, ForeignKey('city.id'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def parse(fp):
    import re
    state_patt = re.compile(r'[0-9]+\. OAB / ([A-Z]{2})')
    city_patt = re.compile(r'[0-9]+\.[0-9]+\. ([^0-9]*)(.*)')
    session = Session()
    state = None
    city = None
    states = set()
    cities = set()
    people = set()
    for line in tqdm(fp.readlines(), ascii=True, desc="Processing text"):
        if m := state_patt.match(line):
            state = m.group(1)
            states.add(state)
        elif m := city_patt.match(line):
            city = m.group(1).strip()
            cities.add((city, state))
            for data in m.group(2).strip(' .').split('/'):
                person_mat, person_name = data.strip().split(', ')
                person_mat = int(person_mat)
                people.add((person_name, person_mat, city))
        else:
            session.rollback()
            return False
    state_ids = dict()
    for state_name in tqdm(states, ascii=True, desc="Storing states"):
        state = State(name=state_name)
        session.add(state)
        session.flush()
        state_ids[state_name] = state.id
    city_ids = dict()
    for (city_name, state_name) in tqdm(cities, ascii=True, desc="Storing cities"):
        state_id = state_ids[state_name]
        city = City(name=city_name, state=state_id)
        session.add(city)
        session.flush()
        city_ids[city_name] = city.id
    for (person_name, person_mat, city_name) in tqdm(people, ascii=True, desc="Storing people"):
        city_id = city_ids[city_name]
        person = Person(name=person_name, mat=person_mat, city=city_id)
        session.add(person)
    session.commit()
    return True

if __name__ == '__main__':
    from sys import argv
    import sqlite3
    assert len(argv) == 2, "Usage: python parse.py <input-file>"
    input_file = argv[1]
    with open(input_file) as fp:
        assert parse(fp)
