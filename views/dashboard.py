from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Label
from commands import COMMANDS
from textual.widgets import Digits



class Dashboard(Vertical):

    def compose(self) -> ComposeResult:
        yield Label("Welcome back!", classes="page-title")
        yield Label("Everything you need, in one place.")

        with Horizontal(id="statistics"):
            with Vertical(classes="stat-card"):
                yield Digits("0", id="contact-count", classes="stat-number")
                yield Label("Total contacts", classes="stat-label")

            with Vertical(classes="stat-card"):
                yield Digits("0", id="birthday-count", classes="stat-number")
                yield Label("Birthdays in 7 days", classes="stat-label")

            with Vertical(classes="stat-card"):
                yield Digits("0", id="note-count", classes="stat-number")
                yield Label("Total notes", classes="stat-label")

        yield Label("Available commands", classes="page-title")

        with Vertical(id="command-list"):
            for command, description in COMMANDS.items():
                with Horizontal(classes="command-row"):
                    yield Label(command, classes="command-name")
                    yield Label(description, classes="command-description")

    def on_mount(self):
        self.refresh_statistics()

    def refresh_statistics(self):
        book = self.app.book

        self.query_one("#contact-count", Digits).update(
            str(len(book))
        )

        self.query_one("#birthday-count", Digits).update(
            str(len(book.get_upcoming_birthdays()))
        )