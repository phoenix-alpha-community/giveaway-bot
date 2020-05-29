import pickle
from config import DATABASE_LOCATION

def db_read_ids() -> dict:
    with open(DATABASE_LOCATION, "rb") as file:
        try:
            contents = pickle.load(file)
        except EOFError:
            contents = {}

    return contents

def db_write_ids(key, entry):
    contents = db_read_ids()
    contents[key] = entry

    with open(DATABASE_LOCATION, "wb") as file:
        pickle.dump(contents, file, protocol=4)
