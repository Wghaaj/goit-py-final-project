from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable


class Contacts(Vertical):
    def compose(self):
        yield Label("Contact Book", classes="page-title")
        yield Label("Manage and view your saved contacts.")

        with Horizontal(id="contact-search"):
            yield Input(placeholder="Search contacts...", id="search-input")
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

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "search-btn":
            query = self.query_one("#search-input", Input).value.strip()
            records = self.app.book.search(query) if query else None
            self.refresh_contacts(records)

    def refresh_contacts(self, records=None):
        table = self.query_one("#contact-table", DataTable)
        table.clear()

        if records is None:
            records = list(self.app.book.values())

        for record in records:
            phones = ", ".join(str(p) for p in record.phones)
            birthday = (
                record.birthday.value.strftime("%d.%m.%Y")
                if record.birthday else "—"
            )
            email = record.email.value if record.email else "—"
            address = record.address.value if record.address else "—"
            table.add_row(record.name.value, phones, email, address, birthday)

        self.query_one("#contact-total", Label).update(
            f"{len(records)} contacts found"
        )
