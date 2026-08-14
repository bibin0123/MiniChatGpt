import tkinter as tk
from tkinter import ttk

from admin.form import AdminForm
from admin.actions import AdminActions


class AdminWindow(tk.Toplevel):

    def __init__(self, parent, on_close=None):

        super().__init__(parent)

        self.on_close_callback = on_close

        self.title("Knowledge Search Pro - Admin")
        self.geometry("950x600")
        self.minsize(800, 500)
        self.resizable(True, True)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.center_window()
        self.create_widgets()

        self.lift()
        self.focus_force()

    # -----------------------------------------

    def close_window(self):

        self.destroy()

        if self.on_close_callback:
            self.on_close_callback()

    # -----------------------------------------

    def center_window(self):

        width = 950
        height = 600

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # -----------------------------------------

    def create_widgets(self):

        header = ttk.Frame(
            self,
            padding=10
        )

        header.pack(side="top", fill="x")

        ttk.Label(
            header,
            text="Knowledge Search Pro - Admin",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")

        # Bottom Status Bar
        self.status = ttk.Label(
            self,
            text="Ready",
            anchor="w"
        )
        self.status.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # Bottom Action Buttons
        button_frame = ttk.Frame(
            self,
            padding=10
        )
        button_frame.pack(
            side="bottom",
            fill="x"
        )

        self.form = AdminForm(self)

        self.actions = AdminActions(
            self.form.storage,
            self.form
        )

        ttk.Button(
            button_frame,
            text="New",
            command=self.actions.new
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Save",
            command=self.actions.save
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Update",
            command=self.actions.update
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.actions.delete
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Smart Paste",
            command=self.actions.smart_paste
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Close",
            command=self.close_window
        ).pack(
            side="right",
            padx=5
        )

        # Main Form packed in remaining space
        self.form.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


