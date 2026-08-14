import tkinter as tk
from tkinter import ttk


class ResultPanel(ttk.Frame):

    def __init__(self, parent, select_callback):

        super().__init__(parent, padding=10)

        self.select_callback = select_callback

        self.create_widgets()

    # -----------------------------------------

    def create_widgets(self):

        ttk.Label(
            self,
            text="Search Results",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("ID", "Title", "Category"),
            show="headings",
            height=18
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Category", text="Category")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Title", width=280)
        self.tree.column("Category", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

    # -----------------------------------------

    def load(self, data):

        self.clear()

        for item in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    item["id"],
                    item["title"],
                    item["category"]
                )
            )

    # -----------------------------------------

    def clear(self):

        self.tree.delete(
            *self.tree.get_children()
        )

    # -----------------------------------------

    def on_select(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        if self.select_callback:

            self.select_callback(
                values[0]
            )

    # -----------------------------------------

    def count(self):

        return len(
            self.tree.get_children()
        )