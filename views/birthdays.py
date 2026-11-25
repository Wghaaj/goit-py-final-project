from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable


class Birthdays(Vertical):

    def compose(self):
        yield Label("Upcoming Birthdays", classes="page-title")
        yield Label("Never miss an important birthday.")

        with Horizontal(id="birthday-search"):
            yield Label("Show birthdays within:")
            yield Input(
                value="7",
                type="integer",
                id="birthday-days"
            )
            yield Label("days")
            yield Button("Search", id="birthday-search-btn")

        yield DataTable(id="birthday-table")
        yield Label("0 upcoming birthdays", id="birthday-total")

    def on_mount(self):
        table = self.query_one("#birthday-table", DataTable)
        table.zebra_stripes = True

        table.add_column("Name", width=25)
        table.add_column("Birthday", width=20)
        table.add_column("Congratulation date", width=25)
        table.cursor_type = "row"

        self.refresh_birthdays()

    def refresh_birthdays(self):
        table = self.query_one("#birthday-table", DataTable)
        table.clear()

        book = self.app.book
        birthdays = book.get_upcoming_birthdays()

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