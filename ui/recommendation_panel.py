import re
import tkinter as tk
from tkinter import ttk


class RecommendationPanel(ttk.Frame):

    def __init__(self, parent, on_select_topic=None):
        super().__init__(parent, padding=12)

        self.on_select_topic = on_select_topic
        self.all_data = []
        self.current_item = None

        self.create_widgets()

    # -----------------------------------------

    def create_widgets(self):
        # Outer Card Frame
        card_frame = tk.Frame(
            self,
            bg="#1E1E1E",
            bd=1,
            relief="solid",
            highlightbackground="#333333",
            highlightthickness=1
        )
        card_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Top Header Bar inside Card
        header_frame = tk.Frame(card_frame, bg="#252526", padx=10, pady=10)
        header_frame.pack(fill="x")

        # Title Label
        self.title_var = tk.StringVar(value="")
        self.title_label = tk.Label(
            header_frame,
            textvariable=self.title_var,
            font=("Segoe UI", 13, "bold"),
            fg="#FFFFFF",
            bg="#252526",
            anchor="w"
        )
        self.title_label.pack(side="left", anchor="w")

        # Category and Tag Badges Frame
        self.badge_frame = tk.Frame(header_frame, bg="#252526")
        self.badge_frame.pack(side="right", anchor="e")

        # Answer Container
        body_frame = tk.Frame(card_frame, bg="#1E1E1E", padx=10, pady=10)
        body_frame.pack(fill="both", expand=True)

        # Code / Text Display Box
        self.answer_text = tk.Text(
            body_frame,
            height=14,
            wrap="word",
            font=("Consolas", 11),
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="#FFFFFF",
            selectbackground="#264F78",
            selectforeground="#FFFFFF",
            bd=0,
            padx=10,
            pady=10,
            relief="flat"
        )
        self.answer_text.pack(fill="both", expand=True)

        # Configure Syntax Highlighting Tags
        self.answer_text.tag_configure("kw_sql", foreground="#569CD6", font=("Consolas", 11, "bold"))
        self.answer_text.tag_configure("kw_py", foreground="#C586C0", font=("Consolas", 11, "bold"))
        self.answer_text.tag_configure("kw_git", foreground="#4EC9B0", font=("Consolas", 11, "bold"))
        self.answer_text.tag_configure("string", foreground="#CE9178")
        self.answer_text.tag_configure("comment", foreground="#6A9955", font=("Consolas", 11, "italic"))
        self.answer_text.tag_configure("number", foreground="#B5CEA8")
        self.answer_text.tag_configure("normal", foreground="#D4D4D4")

        # Bottom Action Bar
        action_bar = tk.Frame(card_frame, bg="#252526", padx=8, pady=8)
        action_bar.pack(fill="x")

        self.copy_btn = tk.Button(
            action_bar,
            text="📋  Copy Full Answer",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#007ACC",
            activebackground="#005999",
            activeforeground="#FFFFFF",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.copy_answer
        )
        self.copy_btn.pack(side="left", padx=(0, 6))

        self.copy_single_btn = tk.Button(
            action_bar,
            text="⚡  Copy Single Line",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#2B5B84",
            activebackground="#1E3E5B",
            activeforeground="#FFFFFF",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.copy_single_line
        )
        self.copy_single_btn.pack(side="left", padx=6)

        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            action_bar,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg="#4EC9B0",
            bg="#252526"
        )
        self.status_label.pack(side="left", padx=12)

    # -----------------------------------------

    def load_recommendations(self, data):
        self.all_data = data
        if data:
            self.show_item(data[0])

    # -----------------------------------------

    def display_search_result(self, search_results, query_text=""):
        if search_results:
            self.show_item(search_results[0])
        else:
            self.current_item = None
            self.title_var.set(f"No results found for '{query_text}'")
            self.update_badges("", [])
            self.answer_text.config(state="normal")
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.insert("1.0", "Try searching with keywords like 'SQL', 'Git', or 'Python'.")
            self.highlight_syntax()
            self.answer_text.config(state="disabled")

    # -----------------------------------------

    def update_badges(self, category, tags):
        for w in self.badge_frame.winfo_children():
            w.destroy()

        if category:
            lbl = tk.Label(
                self.badge_frame,
                text=f" {category.upper()} ",
                font=("Segoe UI", 8, "bold"),
                fg="#38BDF8",
                bg="#0F172A",
                padx=6,
                pady=2,
                bd=1,
                relief="solid"
            )
            lbl.pack(side="left", padx=2)

        for tag in tags:
            lbl = tk.Label(
                self.badge_frame,
                text=f" #{tag} ",
                font=("Segoe UI", 8),
                fg="#A7F3D0",
                bg="#064E3B",
                padx=5,
                pady=2
            )
            lbl.pack(side="left", padx=2)

    # -----------------------------------------

    def show_item(self, item):
        self.current_item = item
        self.title_var.set(item.get("title", ""))
        self.update_badges(item.get("category", ""), item.get("tags", []))

        self.answer_text.config(state="normal")
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", item.get("answer", ""))
        self.highlight_syntax()
        self.answer_text.config(state="disabled")
        self.status_var.set("")

    # -----------------------------------------

    def highlight_syntax(self):
        content = self.answer_text.get("1.0", tk.END)

        for tag in ["kw_sql", "kw_py", "kw_git", "string", "comment", "number"]:
            self.answer_text.tag_remove(tag, "1.0", tk.END)

        sql_keywords = r"\b(CREATE|DATABASE|DROP|SHOW|DATABASES|SELECT|INSERT|INTO|UPDATE|DELETE|FROM|WHERE|TABLE|AND|OR|JOIN|DEFAULT|PRIMARY|KEY)\b"
        py_keywords = r"\b(def|class|import|from|with|as|open|return|if|else|elif|for|in|try|except|print|True|False|None)\b"
        git_keywords = r"\b(git|config|global|init|clone|status|add|commit|push|pull|branch|checkout|merge)\b"

        for match in re.finditer(sql_keywords, content, re.IGNORECASE):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.answer_text.tag_add("kw_sql", start, end)

        for match in re.finditer(py_keywords, content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.answer_text.tag_add("kw_py", start, end)

        for match in re.finditer(git_keywords, content, re.IGNORECASE):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.answer_text.tag_add("kw_git", start, end)

        for match in re.finditer(r"(['\"])(.*?)\1", content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.answer_text.tag_add("string", start, end)

        for match in re.finditer(r"(#|--).*", content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.answer_text.tag_add("comment", start, end)

    # -----------------------------------------

    def get_selected_or_full_text(self):
        try:
            selected = self.answer_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected:
                return selected
        except tk.TclError:
            pass
        return self.answer_text.get("1.0", tk.END).strip()

    # -----------------------------------------

    def copy_answer(self):
        text = self.get_selected_or_full_text()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_var.set("✓ Copied full answer!")
            self.copy_btn.config(bg="#10B981")
            self.after(2000, self.reset_copy_btn)

    # -----------------------------------------

    def copy_single_line(self):
        text = self.get_selected_or_full_text()
        if text:
            # Join multiple lines with space into a single continuous line
            single_line_text = " ".join(line.strip() for line in text.splitlines() if line.strip())
            self.clipboard_clear()
            self.clipboard_append(single_line_text)
            self.status_var.set("⚡ Copied single line!")
            self.copy_single_btn.config(bg="#10B981")
            self.after(2000, self.reset_copy_btn)

    # -----------------------------------------

    def reset_copy_btn(self):
        self.status_var.set("")
        self.copy_btn.config(bg="#007ACC")
        self.copy_single_btn.config(bg="#2B5B84")
