import json
from config import DATABASE_LOCATION

def modify(key: str, text) -> None:
    current = get(full=True)
    k = "giv_ids"
    current[k][key] = text
    file = open(DATABASE_LOCATION, "w")
    json.dump(current, file, indent=4)
    file.close()

def remove(key: str) -> None:
    current = get(full=True)
    k = "giv_ids"
    current[k].pop(key)
    file = open(DATABASE_LOCATION, "w")
    json.dump(current, file, indent=4)
    file.close()

def get(key: str = "giv_ids", full: bool = False) -> [str, list]:
    file = open(DATABASE_LOCATION, "r")
    text = json.load(file)
    file.close()
    if full:
        return text
    return text[key]
