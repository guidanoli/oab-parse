from schema import Session, State, City, Person, HasName, Name, NameType
from sqlalchemy import func

def get_names(state=None, name_type=None):
    session = Session()
    count_ = func.count('*')
    q = session.query(State, City, Person, HasName, Name, count_)\
            .filter(HasName.name==Name.id)\
            .filter(HasName.person==Person.id)\
            .filter(Person.city==City.id)\
            .filter(City.state==State.id)\
            .group_by(Name.name)\
            .order_by(count_.desc())

    if state is not None:
        q = q.filter(State.name==state)

    if name_type is not None:
        q = q.filter(Name.type==name_type)

    for row in q.all():
        yield row[-1], row.Name

if __name__ == '__main__':
    from sys import argv
    argc = len(argv)
    
    if argc >= 2:
        state = argv[1]
        if argc >= 3:
            name_type = None
            for nt in NameType:
                if nt.name == argv[2]:
                    name_type = nt
                    break
            assert name_type is not None
            gen = get_names(state, name_type)
        else:
            gen = get_names(state)
    else:
        gen = get_names()

    for count, name in gen:
        print(count, name.name, name.type)
