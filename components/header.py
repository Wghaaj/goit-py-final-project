from textual.containers import Vertical
from textual.widgets import Label


class AppHeader(Vertical):

    def compose(self):
        yield Label("PERSONAL ASSISTANT", id="app-title")
        yield Label(
            "Contacts · Birthdays · Notes",
            id="app-subtitle"
        )