from schema import Session, State, City, Person, HasName, Name
from sqlalchemy import func

def get_states():
    session = Session()
    q = session.query(State)\
            .order_by(State.name)
    for row in q.all():
        print(row.name)

if __name__ == '__main__':
    get_states()
