import tkinter as tk
from tkinter import ttk
import re


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

        # ---------------- Meta Header Grid ----------------

        meta_frame = ttk.Frame(self)
        meta_frame.pack(fill="x", pady=(0, 10))

        # Title
        ttk.Label(
            meta_frame,
            text="Title:",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=2)

        self.title_label = ttk.Label(
            meta_frame,
            text="-",
            font=("Segoe UI", 10, "bold"),
            foreground="#0056b3"
        )
        self.title_label.grid(row=0, column=1, sticky="w", pady=2)

        # Category
        ttk.Label(
            meta_frame,
            text="Category:",
            font=("Segoe UI", 10, "bold")
        ).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=2)

        self.category_label = ttk.Label(
            meta_frame,
            text="-"
        )
        self.category_label.grid(row=1, column=1, sticky="w", pady=2)

        # Keywords
        ttk.Label(
            meta_frame,
            text="Keywords:",
            font=("Segoe UI", 10, "bold")
        ).grid(row=2, column=0, sticky="w", padx=(0, 5), pady=2)

        self.keyword_label = ttk.Label(
            meta_frame,
            text="-",
            wraplength=450
        )
        self.keyword_label.grid(row=2, column=1, sticky="w", pady=2)

        # Tags
        ttk.Label(
            meta_frame,
            text="Tags:",
            font=("Segoe UI", 10, "bold")
        ).grid(row=3, column=0, sticky="w", padx=(0, 5), pady=2)

        self.tag_label = ttk.Label(
            meta_frame,
            text="-",
            wraplength=450
        )
        self.tag_label.grid(row=3, column=1, sticky="w", pady=2)

        # ---------------- Answer ----------------

        ttk.Label(
            self,
            text="Answer Details",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(10, 2))

        # Text container with scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, pady=5)

        self.scrollbar = ttk.Scrollbar(text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.answer_text = tk.Text(
            text_frame,
            height=15,
            wrap="word",
            font=("Segoe UI", 10),
            yscrollcommand=self.scrollbar.set,
            padx=10,
            pady=10,
            bg="#fbfbfb",
            relief="solid",
            bd=1
        )

        self.answer_text.pack(
            side="left",
            fill="both",
            expand=True
        )
        self.scrollbar.config(command=self.answer_text.yview)

        # Configure Text Tags for Rich Formatting
        self.answer_text.tag_config("heading", font=("Segoe UI", 11, "bold"), foreground="#1a252f", spacing1=8, spacing3=4)
        self.answer_text.tag_config("bold", font=("Segoe UI", 10, "bold"))
        self.answer_text.tag_config("code_block", font=("Consolas", 9.5), background="#eef2f7", foreground="#24292e", lmargin1=15, lmargin2=15, rmargin=15, spacing1=4, spacing3=4)
        self.answer_text.tag_config("list_item", font=("Segoe UI", 10), lmargin1=15, lmargin2=25)
        self.answer_text.tag_config("normal", font=("Segoe UI", 10), foreground="#212529", spacing3=4)

        self.answer_text.config(
            state="disabled"
        )

        # ---------------- Buttons ----------------

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(
            button_frame,
            text="Copy Answer",
            command=self.copy_answer
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear
        ).pack(side="left", padx=5)

    # -----------------------------------------

    def render_formatted_answer(self, raw_text):
        """Parse raw text/markdown and insert styled text tags into tk.Text"""
        if not raw_text:
            return

        lines = raw_text.splitlines()
        in_code_block = False

        for i, line in enumerate(lines):
            line_str = line

            if line_str.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                self.answer_text.insert("end", line_str + "\n", "code_block")
                continue

            # Heading check (Markdown **bold heading** or # heading)
            bold_match = re.match(r"^\*\*(.*?)\*\*$", line_str.strip())
            header_match = re.match(r"^\#+\s*(.*)$", line_str.strip())

            if bold_match:
                clean_heading = bold_match.group(1)
                self.answer_text.insert("end", clean_heading + "\n", "heading")
            elif header_match:
                clean_heading = header_match.group(1)
                self.answer_text.insert("end", clean_heading + "\n", "heading")
            elif line_str.strip().startswith(("- ", "* ", "• ")) or re.match(r"^\d+[\.\)]\s+", line_str.strip()):
                # Bullet or Numbered List Item
                self.answer_text.insert("end", line_str + "\n", "list_item")
            else:
                # Inline bold parsing for normal text
                parts = re.split(r"(\*\*.*?\*\*)", line_str)
                for part in parts:
                    if part.startswith("**") and part.endswith("**") and len(part) > 4:
                        self.answer_text.insert("end", part[2:-2], "bold")
                    else:
                        self.answer_text.insert("end", part, "normal")
                self.answer_text.insert("end", "\n", "normal")

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

        self.render_formatted_answer(item.get("answer", ""))

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