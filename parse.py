from tqdm import tqdm
from schema import Session, State, City, Person, HasName, Name, NameType

def normalize_names(names):
    return tuple(name.title() for name in names)

def categorize_name(name, new_name_type, name_types):
    type_dict = name_types.get(name)
    if type_dict is None:
        name_types[name] = {new_name_type: 1}
    else:
        old_count = type_dict.get(new_name_type, 0)
        type_dict[new_name_type] = old_count + 1

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
                person_number, person_name = data.strip().split(', ')
                person_names = normalize_names(person_name.split())
                people.add((person_names, person_number, city))
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
    name_type_candidates = dict()
    for (person_names, _, _) in tqdm(people, ascii=True, desc="Analysing names 1/2"):
        # assume at first that the first name is always a Forename
        # and that the other ones are surenames
        categorize_name(person_names[0], NameType.Forename, name_type_candidates)
        for person_name in person_names[1:]:
            categorize_name(person_name, NameType.Surname, name_type_candidates)
    name_types = dict()
    for (name, type_dict) in tqdm(name_type_candidates.items(), ascii=True, desc="Analysing names 2/2"):
        # choose the most common type. on draw, make it 'Unknown'
        winning_items = sorted(type_dict.items(), key=lambda t: t[1], reverse=True)[:2]
        if len(winning_items) > 1 and winning_items[0][1] == winning_items[1][1]:
            name_types[name] = NameType.Unknown
        else:
            name_types[name] = winning_items[0][0]
    name_ids = dict()
    for (person_names, person_number, city_name) in tqdm(people, ascii=True, desc="Storing people"):
        city_id = city_ids[city_name]
        fullname = ' '.join(person_names)
        person = Person(city=city_id, number=person_number, fullname=fullname)
        session.add(person)
        session.flush()
        person_names_count = len(person_names)
        for name_pos, name_str in enumerate(person_names):
            if name_str not in name_ids:
                name_type = name_types[name_str]
                name = Name(name=name_str, type=name_type)
                session.add(name)
                session.flush()
                name_ids[name_str] = name.id
            name_id = name_ids[name_str]
            has_name = HasName(name=name_id, person=person.id, position=name_pos+1)
            session.add(has_name)
    session.commit()
    return True

if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 2, "Usage: python parse.py <input-file>"
    input_file = argv[1]
    with open(input_file) as fp:
        assert parse(fp)
