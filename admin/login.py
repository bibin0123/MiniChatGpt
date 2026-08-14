import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


class LoginWindow(tk.Toplevel):

    def __init__(self, parent, on_success):

        super().__init__(parent)

        self.on_success = on_success
        self.config_file = Path("data/config.json")

        self.title("Admin Login")
        self.geometry("380x270")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.center_window()

        self.create_variables()
        self.create_widgets()

        self.username_entry.focus()

    # -----------------------------------------

    def center_window(self):

        width = 380
        height = 270

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    # -----------------------------------------

    def create_variables(self):

        self.username = tk.StringVar()
        self.password = tk.StringVar()

    # -----------------------------------------

    def create_widgets(self):

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Administrator Login",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 15))

        ttk.Label(frame, text="Username").pack(anchor="w")

        self.username_entry = ttk.Entry(
            frame,
            textvariable=self.username
        )

        self.username_entry.pack(fill="x", pady=(2, 10))

        ttk.Label(frame, text="Password").pack(anchor="w")

        password_entry = ttk.Entry(
            frame,
            textvariable=self.password,
            show="*"
        )

        password_entry.pack(fill="x", pady=(2, 15))

        password_entry.bind(
            "<Return>",
            lambda e: self.login()
        )

        button_frame = ttk.Frame(frame)
        button_frame.pack(side="bottom", fill="x")

        ttk.Button(
            button_frame,
            text="Login",
            command=self.login
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side="left", expand=True, fill="x")

    # -----------------------------------------

    def login(self):

        if not self.config_file.exists():
            messagebox.showerror(
                "Error",
                "config.json not found."
            )

            return

        with open(
                self.config_file,
                "r",
                encoding="utf-8"
        ) as file:

            config = json.load(file)

        username = self.username.get().strip()
        password = self.password.get()

        if (
                username == config["admin_username"]
                and
                password == config["admin_password"]
        ):

            self.destroy()

            if self.on_success:
                self.on_success()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

            self.password.set("")
            self.username_entry.focus()