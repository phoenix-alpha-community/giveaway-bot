"""
This module implements the persistency necessary to preserve
giveaways across bot restarts.
"""

import pickle
from config import DATABASE_LOCATION

def db_read_ids() -> dict:
    """
    Read the contents of the database.

    Attributes:
        None

    Returns:
        dict: The contents of the database.
    """

    # Open the database and return the contents
    with open(DATABASE_LOCATION, "rb") as file:
        try:
            contents = pickle.load(file)
        except EOFError:
            contents = {}  # If the database is empty return empty dict

    return contents


def db_write_ids(key, value) -> None:
    """
    Adds an entry to the database.

    Attributes:
        key (any type): The name of the entry in the database.
        value (any type): The value of the entry.

    Returns:
        None
    """

    contents = db_read_ids()  # Get the contents of the database
    contents[key] = value  # Add the entry to the contents

    # Save the updated contents in the database
    with open(DATABASE_LOCATION, "wb") as file:
        pickle.dump(contents, file, protocol=4)


def db_remove_ids(*entry) -> None:
    """
    Removes an number of entries from the database.

    Attributes:
        entry (any type): Entry to be removed from the database.

    Returns:
        None
    """

    contents = db_read_ids()  # Get the contents of the database

    # Remove the database entries from the contents
    for k in entry:
        contents.pop(k)

    # Save the updated contents in the database
    with open(DATABASE_LOCATION, "wb") as file:
        pickle.dump(contents, file, protocol=4)
