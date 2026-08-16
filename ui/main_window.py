import tkinter as tk
from tkinter import ttk

from ui.search_panel import SearchPanel
from ui.recommendation_panel import RecommendationPanel

from core.storage import Storage
from core.search import SearchEngine

from admin.login import LoginWindow
from admin.window import AdminWindow


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.storage = Storage()
        self.search_engine = SearchEngine()

        self.title("Knowledge Search Pro")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.resizable(True, True)

        self.current_data = []
        self.login_window = None
        self.admin_window = None

        self.create_widgets()
        self.load_data()

    # -----------------------------------------

    def create_widgets(self):
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Knowledge Search Pro",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

        ttk.Button(
            header,
            text="Admin",
            command=self.open_login
        ).pack(side="right")

        self.search_panel = SearchPanel(
            self,
            self.search
        )
        self.search_panel.pack(fill="x")

        self.recommendation_panel = RecommendationPanel(
            self,
            on_select_topic=self.on_topic_selected
        )
        self.recommendation_panel.pack(fill="both", expand=True)

    # -----------------------------------------

    def load_data(self):
        self.current_data = self.storage.load()
        self.search_panel.set_knowledge_data(self.current_data)
        self.recommendation_panel.load_recommendations(self.current_data)

    # -----------------------------------------

    def search(self, text):
        if not text.strip():
            self.recommendation_panel.load_recommendations(self.current_data)
            return

        result = self.search_engine.search(
            self.current_data,
            text
        )
        self.recommendation_panel.display_search_result(result, text)

    # -----------------------------------------

    def on_topic_selected(self, topic_title):
        self.search_panel.search_text.set(topic_title)

    # -----------------------------------------

    def open_login(self):
        if self.admin_window is not None and self.admin_window.winfo_exists():
            self.admin_window.lift()
            self.admin_window.focus_force()
            return

        if self.login_window is not None and self.login_window.winfo_exists():
            self.login_window.lift()
            self.login_window.focus_force()
            return

        self.login_window = LoginWindow(
            self,
            self.open_admin
        )

    # -----------------------------------------

    def open_admin(self):
        self.withdraw()

        self.admin_window = AdminWindow(
            self,
            on_close=self.on_admin_close
        )

    # -----------------------------------------

    def on_admin_close(self):
        self.deiconify()
        self.load_data()