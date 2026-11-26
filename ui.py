from textual.app import App, ComposeResult
from textual.widgets import Footer, TabbedContent, TabPane, Input, RichLog
from rich.text import Text

from components.header import AppHeader
from components.command_input import CommandInput
from components.confirmation import Confirmation

from views.dashboard import Dashboard
from views.contacts import Contacts
from views.birthdays import Birthdays
from views.notes import Notes

from command_handler import execute_command
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
        "styles/confirmation.tcss",
    ]

    def __init__(self):
        super().__init__()
        self.book, self.notebook = load_data()

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

        yield RichLog(id="command-output", wrap=True)
        yield CommandInput()
        yield Footer()

    # Handle submitted commands
    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id != "command":
            return

        command, args = parse_input(event.value)
        event.input.value = ""

        if not command:
            return

        if command in ("remove", "delete-note") and len(args) == 1:
            self.push_screen(
                Confirmation(),
                lambda confirmed: self.process_command(command, args)
                if confirmed else None
            )
        else:
            self.process_command(command, args)

    # Execute commands
    def process_command(self, command, args):
        output = self.query_one("#command-output", RichLog)

        if command == "exit":
            save_data(self.book, self.notebook)
            self.exit()
            return

        if command == "hello":
            output.write("How can I help you?")
            return

        result = execute_command(
            command, args, self.book, self.notebook
        )

        output.write(Text.from_ansi(result))

        save_data(self.book, self.notebook)
        self.refresh_views()

    # Refresh displayed data
    def refresh_views(self):
        self.query_one(Dashboard).refresh_statistics()
        self.query_one(Contacts).refresh_contacts()
        self.query_one(Birthdays).refresh_birthdays()
        self.query_one(Notes).refresh_notes()


if __name__ == "__main__":
    AssistantApp().run()