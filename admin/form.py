import tkinter as tk
from tkinter import ttk

from core.storage import Storage


class AdminForm(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.storage = Storage()

        self.selected_id = None

        self.create_variables()
        self.create_widgets()

        self.load_tree()

    # -----------------------------------------

    def create_variables(self):

        self.title_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.keyword_var = tk.StringVar()
        self.tag_var = tk.StringVar()

    # -----------------------------------------

    def create_widgets(self):

        # ---------- Tree ----------

        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Title", "Category"),
            show="headings",
            height=8
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Category", text="Category")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Title", width=350)
        self.tree.column("Category", width=120)

        self.tree.pack(fill="x", pady=10)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_item
        )

        # ---------- Title ----------

        ttk.Label(
            self,
            text="Title"
        ).pack(anchor="w")

        ttk.Entry(
            self,
            textvariable=self.title_var
        ).pack(fill="x", pady=5)

        # ---------- Category ----------

        ttk.Label(
            self,
            text="Category"
        ).pack(anchor="w")

        self.category = ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=[
                "SQL",
                "Python",
                "Tkinter",
                "React",
                "Django",
                "Linux",
                "General"
            ],
            state="readonly"
        )

        self.category.pack(fill="x", pady=5)

        # ---------- Keywords ----------

        ttk.Label(
            self,
            text="Keywords"
        ).pack(anchor="w")

        ttk.Entry(
            self,
            textvariable=self.keyword_var
        ).pack(fill="x", pady=5)

        # ---------- Tags ----------

        ttk.Label(
            self,
            text="Tags"
        ).pack(anchor="w")

        ttk.Entry(
            self,
            textvariable=self.tag_var
        ).pack(fill="x", pady=5)

        # ---------- Answer ----------

        ttk.Label(
            self,
            text="Answer"
        ).pack(anchor="w")

        self.answer_text = tk.Text(
            self,
            height=12,
            wrap="word"
        )

        self.answer_text.pack(
            fill="both",
            expand=True,
            pady=5
        )

    # -----------------------------------------

    def load_tree(self):

        self.tree.delete(
            *self.tree.get_children()
        )

        data = self.storage.load()

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

    def select_item(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_id = values[0]

        data = self.storage.load()

        for item in data:

            if item["id"] == self.selected_id:

                self.title_var.set(
                    item["title"]
                )

                self.category_var.set(
                    item["category"]
                )

                self.keyword_var.set(
                    ",".join(
                        item["keywords"]
                    )
                )

                self.tag_var.set(
                    ",".join(
                        item.get("tags", [])
                    )
                )

                self.answer_text.delete(
                    "1.0",
                    tk.END
                )

                self.answer_text.insert(
                    "1.0",
                    item["answer"]
                )

                break
