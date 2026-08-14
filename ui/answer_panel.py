import tkinter as tk
from tkinter import ttk


class AnswerPanel(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent, padding=10)

        self.create_widgets()

    # -----------------------------------------

    def create_widgets(self):

        ttk.Label(
            self,
            text="Knowledge Details",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 10))

        # ---------------- Title ----------------

        ttk.Label(
            self,
            text="Title",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.title_label = ttk.Label(
            self,
            text="-"
        )

        self.title_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # ---------------- Category ----------------

        ttk.Label(
            self,
            text="Category",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.category_label = ttk.Label(
            self,
            text="-"
        )

        self.category_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # ---------------- Keywords ----------------

        ttk.Label(
            self,
            text="Keywords",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.keyword_label = ttk.Label(
            self,
            text="-",
            wraplength=500
        )

        self.keyword_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # ---------------- Tags ----------------

        ttk.Label(
            self,
            text="Tags",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.tag_label = ttk.Label(
            self,
            text="-",
            wraplength=500
        )

        self.tag_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # ---------------- Answer ----------------

        ttk.Label(
            self,
            text="Answer",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.answer_text = tk.Text(
            self,
            height=15,
            wrap="word",
            font=("Consolas", 11)
        )

        self.answer_text.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.answer_text.config(
            state="disabled"
        )

        # ---------------- Buttons ----------------

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(
            button_frame,
            text="Copy",
            command=self.copy_answer
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear
        ).pack(side="left", padx=5)

    # -----------------------------------------

    def load(self, item):

        self.title_label.config(
            text=item.get("title", "-")
        )

        self.category_label.config(
            text=item.get("category", "-")
        )

        self.keyword_label.config(
            text=", ".join(
                item.get("keywords", [])
            )
        )

        self.tag_label.config(
            text=", ".join(
                item.get("tags", [])
            )
        )

        self.answer_text.config(
            state="normal"
        )

        self.answer_text.delete(
            "1.0",
            tk.END
        )

        self.answer_text.insert(
            "1.0",
            item.get("answer", "")
        )

        self.answer_text.config(
            state="disabled"
        )

    # -----------------------------------------

    def clear(self):

        self.title_label.config(text="-")
        self.category_label.config(text="-")
        self.keyword_label.config(text="-")
        self.tag_label.config(text="-")

        self.answer_text.config(
            state="normal"
        )

        self.answer_text.delete(
            "1.0",
            tk.END
        )

        self.answer_text.config(
            state="disabled"
        )

    # -----------------------------------------

    def copy_answer(self):

        text = self.answer_text.get(
            "1.0",
            tk.END
        ).strip()

        if text:

            self.clipboard_clear()
            self.clipboard_append(text)