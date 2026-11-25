from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import ( 
    Footer, TabbedContent,
    TabPane, Label, Input
)
from views.dashboard import Dashboard
from views.contacts import Contacts
from views.birthdays import Birthdays
from views.notes import Notes
from commands import COMMANDS

from storage import load_data


class AssistantApp(App):
    def __init__(self):
        super().__init__()
        self.book = load_data()

    TITLE = "Personal Assistant"
    CSS_PATH = [
        "styles/global.tcss",
        "styles/dashboard.tcss",
        "styles/contacts.tcss",
        "styles/birthdays.tcss",
        "styles/notes.tcss",
    ]

    def compose(self) -> ComposeResult:
        #header
        with Vertical(id="app-header"):
            yield Label("PERSONAL ASSISTANT", id="app-title")
            yield Label(
                "Contacts · Birthdays · Notes",
                id="app-subtitle"
            )

        #tabs
        with TabbedContent():
            with TabPane("Dashboard"):
                yield Dashboard()

            with TabPane("Contacts"):
                yield Contacts()

            with TabPane("Birthdays"):
                yield Birthdays()

            with TabPane("Notes"):
                yield Notes()

        #user input
        yield Input(
            placeholder="Enter a command...",
            id="command"
        )

        yield Footer()

if __name__ == "__main__":
    AssistantApp().run()