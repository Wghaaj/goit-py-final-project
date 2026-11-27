"""Save and load contacts and notes using pickle."""

import pickle

from models import AddressBook
from notes import Notebook


def save_data(book, notebook, filename="addressbook.pkl"):
    # Store contacts and notes together in one file.
    payload = {
        "book": book,
        "notebook": notebook,
    }

    with open(filename, "wb") as file:
        pickle.dump(payload, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)

    except FileNotFoundError:
        return AddressBook(), Notebook()

    # Support older save files containing only contacts.
    if isinstance(data, AddressBook):
        return data, Notebook()

    # Restore both collections from the current save format.
    if isinstance(data, dict):
        book = data.get("book")
        notebook = data.get("notebook")

        return (
            book if isinstance(book, AddressBook) else AddressBook(),
            notebook if isinstance(notebook, Notebook) else Notebook(),
        )

    return AddressBook(), Notebook()