from schema import Session, Name, NameType
from names import get_names

type_names = {
    "u": NameType.Unknown,
    "f": NameType.Forename,
    "s": NameType.Surname,
    "o": NameType.other,
}

def sort(state=None):
    session = Session()
    for cnt, name in get_names(state):
        if name.type != NameType.Unknown:
            continue
        type_name = input("{} -- [f]orename/[s]urname/[o]thers/[u]nknown/e[x]it? ".format(name.name)).lower()
        type = type_names.get(type_name)
        if type is not None:
            name.type = type
            session.commit()
        else:
            return False

if __name__ == '__main__':
    from sys import argv
    if len(argv) >= 2:
        state = argv[1]
        sort(state)
    else:
        sort()
