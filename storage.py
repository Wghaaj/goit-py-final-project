"""Save and load the address book using pickle."""

import pickle
from models import AddressBook
from notes import Notebook


def save_data(book, notebook, filename="addressbook.pkl"):
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

    if isinstance(data, AddressBook):
        return data, Notebook()

    if isinstance(data, dict):
        book = data.get("book")
        notebook = data.get("notebook")
        return (
            book if isinstance(book, AddressBook) else AddressBook(),
            notebook if isinstance(notebook, Notebook) else Notebook(),
        )

    return AddressBook(), Notebook()
