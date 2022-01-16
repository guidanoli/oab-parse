from schema import Session, State, City, Person, HasName, Name
from sqlalchemy import func

def get_states():
    session = Session()
    q = session.query(State)\
            .order_by(State.name)
    for row in q.all():
        yield row.name

if __name__ == '__main__':
    for state in get_states():
        print(state)
