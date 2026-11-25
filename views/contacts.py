from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable


class Contacts(Vertical):

    def compose(self):
        yield Label("Contact Book", classes="page-title")
        yield Label("Manage and view your saved contacts.")

        with Horizontal(id="contact-search"):
            yield Input(
                placeholder="Search contacts...",
                id="search-input"
            )
            yield Button("Search", id="search-btn")

        yield DataTable(id="contact-table")
        yield Label("0 contacts found", id="contact-total")

    def on_mount(self):
        table = self.query_one("#contact-table", DataTable)
        table.zebra_stripes = True

        table.add_column("Name", width=20)
        table.add_column("Phone", width=18)
        table.add_column("Email", width=28)
        table.add_column("Address", width=25)
        table.add_column("Birthday", width=15)
        table.cursor_type = "row"

        self.refresh_contacts()

    def refresh_contacts(self):
        table = self.query_one("#contact-table", DataTable)
        table.clear()

        book = self.app.book

        for record in book.data.values():
            phones = ", ".join(str(p) for p in record.phones)

            birthday = (
                record.birthday.value.strftime("%d.%m.%Y")
                if record.birthday else "—"
            )

            table.add_row(
                record.name.value,
                phones,
                "—",
                "—",
                birthday
            )

        self.query_one("#contact-total", Label).update(
            f"{len(book)} contacts found"
        )