from textual.app import App, ComposeResult
from textual.widgets import Footer, TabbedContent, TabPane, Input
from rich.text import Text

from components.header import AppHeader
from components.command_input import CommandInput

from views.dashboard import Dashboard
from views.contacts import Contacts
from views.birthdays import Birthdays
from views.notes import Notes

from command_handler import COMMAND_HANDLERS
from storage import load_data, save_data
from utils import parse_input


class AssistantApp(App):
    TITLE = "Personal Assistant"

    CSS_PATH = [
        "styles/global.tcss",
        "styles/dashboard.tcss",
        "styles/contacts.tcss",
        "styles/birthdays.tcss",
        "styles/notes.tcss",
        "styles/command_input.tcss",
    ]

    def __init__(self):
        super().__init__()
        self.book = load_data()

        # Compatibility with previously saved contacts
        for record in self.book.data.values():
            if not hasattr(record, "email"):
                record.email = None
            if not hasattr(record, "address"):
                record.address = None

    def compose(self) -> ComposeResult:

        yield AppHeader(id="app-header")

        with TabbedContent():
            with TabPane("Dashboard"):
                yield Dashboard()

            with TabPane("Contacts"):
                yield Contacts()

            with TabPane("Birthdays"):
                yield Birthdays()

            with TabPane("Notes"):
                yield Notes()

        yield CommandInput()
        yield Footer()

    # Execute submitted commands
    def on_input_submitted(self, event: Input.Submitted):

        if event.input.id != "command":
            return

        command, args = parse_input(event.value)
        event.input.value = ""

        if not command:
            return

        if command == "exit":
            save_data(self.book)
            self.exit()
            return

        if command == "hello":
            self.notify("How can I help you?")
            return

        handler = COMMAND_HANDLERS.get(command)

        if handler is None:
            self.notify("Invalid command.", severity="error")
            return

        result = handler(args, self.book)

        # Remove Colorama formatting
        message = Text.from_ansi(str(result)).plain

        if message.startswith("Error:"):
            self.notify(message, severity="error")
            return

        self.notify(message)

        save_data(self.book)
        self.refresh_views()

    # Refresh displayed data
    def refresh_views(self):
        self.query_one(Dashboard).refresh_statistics()
        self.query_one(Contacts).refresh_contacts()
        self.query_one(Birthdays).refresh_birthdays()


if __name__ == "__main__":
    AssistantApp().run()