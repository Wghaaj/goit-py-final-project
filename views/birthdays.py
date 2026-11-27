"""Upcoming birthdays view with a configurable search period."""

from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable


class Birthdays(Vertical):
    def __init__(self):
        super().__init__()
        self.days = 7

    def compose(self):
        yield Label("Upcoming Birthdays", classes="page-title")
        yield Label("Never miss an important birthday.")

        with Horizontal(id="birthday-search"):
            yield Label("Show birthdays within:")
            yield Input(value="7", type="integer", id="birthday-days")
            yield Label("days")
            yield Button("Search", id="birthday-search-btn")

        yield DataTable(id="birthday-table")
        yield Label("0 upcoming birthdays", id="birthday-total")

    def on_mount(self):
        table = self.query_one("#birthday-table", DataTable)
        table.zebra_stripes = True
        table.cursor_type = "row"

        table.add_column("Name", width=25)
        table.add_column("Birthday", width=20)
        table.add_column("Congratulation date", width=25)

        self.refresh_birthdays()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "birthday-search-btn":
            self.search_birthdays()

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "birthday-days":
            self.search_birthdays()
            event.stop()

    def search_birthdays(self):
        value = self.query_one("#birthday-days", Input).value

        # Validate the search period before updating the table.
        try:
            days = int(value)

            if not 1 <= days <= 365:
                raise ValueError

        except ValueError:
            self.app.notify(
                "Enter a whole number between 1 and 365.",
                severity="error"
            )
            return

        self.days = days
        self.refresh_birthdays()

    def refresh_birthdays(self):
        table = self.query_one("#birthday-table", DataTable)
        table.clear()

        book = self.app.book

        # Preserve the selected search period when refreshing.
        birthdays = book.get_upcoming_birthdays(self.days)

        for person in birthdays:
            record = book.find(person["name"])

            table.add_row(
                person["name"],
                record.birthday.value.strftime("%d.%m"),
                person["congratulation_date"]
            )

        self.query_one("#birthday-total", Label).update(
            f"{len(birthdays)} upcoming birthdays"
        )