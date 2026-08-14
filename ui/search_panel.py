import tkinter as tk
from tkinter import ttk


class SearchPanel(ttk.Frame):

    def __init__(self, parent, search_callback):

        super().__init__(parent, padding=10)

        self.search_callback = search_callback

        self.search_text = tk.StringVar()

        self.create_widgets()

    # -----------------------------------------

    def create_widgets(self):

        ttk.Label(
            self,
            text="Search",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        frame = ttk.Frame(self)

        frame.pack(fill="x")

        self.entry = ttk.Entry(
            frame,
            textvariable=self.search_text,
            font=("Segoe UI", 11)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ttk.Button(
            frame,
            text="Search",
            command=self.search
        ).pack(side="right")

        self.entry.bind(
            "<Return>",
            lambda e: self.search()
        )

        self.entry.focus()

    # -----------------------------------------

    def search(self):

        if self.search_callback:

            self.search_callback(

                self.search_text.get()

            )

    # -----------------------------------------

    def clear(self):

        self.search_text.set("")

        self.entry.focus()

    # -----------------------------------------

    def get_text(self):

        return self.search_text.get()