import tkinter as tk
from tkinter import ttk


class SearchPanel(ttk.Frame):

    def __init__(self, parent, search_callback):
        super().__init__(parent, padding=10)

        self.search_callback = search_callback
        self.search_text = tk.StringVar()
        self.knowledge_data = []

        self.popup = None
        self.listbox = None
        self.filtered_items = []

        self.create_widgets()

    # -----------------------------------------

    def create_widgets(self):
        ttk.Label(
            self,
            text="Search",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

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

        # Key & Focus Event bindings for autocomplete dropdown
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<Return>", lambda e: self.on_enter_pressed())
        self.entry.bind("<Down>", self.on_down_arrow)
        self.entry.bind("<FocusOut>", self.on_focus_out)

        self.entry.focus()

    # -----------------------------------------

    def set_knowledge_data(self, data):
        self.knowledge_data = data

    # -----------------------------------------

    def on_key_release(self, event):
        # Ignore navigation keys
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return

        query = self.search_text.get().strip().lower()

        if not query or not self.knowledge_data:
            self.hide_popup()
            if self.search_callback:
                self.search_callback("")
            return

        # Match titles, categories, keywords, tags starting with or containing query
        prefix_matches = []
        substring_matches = []

        for item in self.knowledge_data:
            title = item.get("title", "")
            title_lower = title.lower()
            category = item.get("category", "").lower()
            keywords = [k.lower() for k in item.get("keywords", [])]
            tags = [t.lower() for t in item.get("tags", [])]

            if (title_lower.startswith(query) or category.startswith(query) or
                    any(k.startswith(query) for k in keywords) or
                    any(t.startswith(query) for t in tags)):
                if item not in prefix_matches:
                    prefix_matches.append(item)
            elif (query in title_lower or query in category or
                  any(query in k for k in keywords) or
                  any(query in t for t in tags)):
                if item not in substring_matches:
                    substring_matches.append(item)

        self.filtered_items = prefix_matches + substring_matches

        if self.filtered_items:
            self.show_popup()
        else:
            self.hide_popup()

        # Trigger live search filtering
        if self.search_callback:
            self.search_callback(self.search_text.get())

    # -----------------------------------------

    def show_popup(self):
        if not self.popup or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self)
            self.popup.wm_overrideredirect(True)
            self.popup.attributes("-topmost", True)

            self.listbox = tk.Listbox(
                self.popup,
                font=("Segoe UI", 10),
                selectbackground="#0078D7",
                selectforeground="white",
                activestyle="none",
                bd=1,
                relief="solid"
            )
            self.listbox.pack(fill="both", expand=True)

            self.listbox.bind("<ButtonRelease-1>", self.on_select_item)
            self.listbox.bind("<Return>", self.on_select_item)

        self.listbox.delete(0, tk.END)
        for item in self.filtered_items:
            display_str = item.get("title", "")
            cat = item.get("category", "")
            if cat:
                display_str += f"  ({cat})"
            self.listbox.insert(tk.END, display_str)

        # Position dropdown right below the entry box
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height() + 2
        width = self.entry.winfo_width()
        height = min(len(self.filtered_items) * 24 + 6, 180)

        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        self.popup.deiconify()

    # -----------------------------------------

    def hide_popup(self):
        if self.popup and self.popup.winfo_exists():
            self.popup.withdraw()

    # -----------------------------------------

    def on_down_arrow(self, event):
        if self.popup and self.popup.winfo_exists() and self.popup.state() == "normal":
            self.listbox.focus_set()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    # -----------------------------------------

    def on_select_item(self, event=None):
        if not self.listbox:
            return

        sel = self.listbox.curselection()
        if sel:
            index = sel[0]
            selected_item = self.filtered_items[index]
            self.search_text.set(selected_item.get("title", ""))
            self.hide_popup()
            self.entry.focus()
            self.search()

    # -----------------------------------------

    def on_enter_pressed(self):
        self.hide_popup()
        self.search()

    # -----------------------------------------

    def on_focus_out(self, event):
        # Small delay to allow clicking listbox items
        self.after(200, self.check_focus_and_hide)

    # -----------------------------------------

    def check_focus_and_hide(self):
        focused = self.focus_get()
        if self.listbox and focused == self.listbox:
            return
        if self.popup and focused == self.popup:
            return
        self.hide_popup()

    # -----------------------------------------

    def search(self):
        self.hide_popup()
        if self.search_callback:
            self.search_callback(self.search_text.get())

    # -----------------------------------------

    def clear(self):
        self.search_text.set("")
        self.hide_popup()
        self.entry.focus()

    # -----------------------------------------

    def get_text(self):
        return self.search_text.get()