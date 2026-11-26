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

        commands = list(COMMANDS.values())
        middle = (len(commands) + 1) // 2

        with Horizontal(id="command-list"):
            for column in (commands[:middle], commands[middle:]):
                with Vertical(classes="command-column"):
                    for command in column:
                        yield Label(command, classes="command-syntax")

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

        self.query_one("#note-count", Digits).update(
            str(len(self.app.notebook))
        )
