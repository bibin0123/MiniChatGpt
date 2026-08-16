from tkinter import messagebox


class AdminActions:

    def __init__(self, storage, form):

        self.storage = storage
        self.form = form

    # -----------------------------------------
    # New
    # -----------------------------------------

    def new(self):

        self.form.selected_id = None

        self.form.title_var.set("")
        self.form.category_var.set("")
        self.form.keyword_var.set("")
        self.form.tag_var.set("")

        self.form.answer_text.delete(
            "1.0",
            "end"
        )

    # -----------------------------------------
    # Save
    # -----------------------------------------

    def save(self):

        title = self.form.title_var.get().strip()

        if title == "":

            messagebox.showwarning(
                "Warning",
                "Title is required."
            )

            return

        item = {

            "title": title,

            "category":
                self.form.category_var.get(),

            "keywords":

                [

                    x.strip()

                    for x in

                    self.form.keyword_var
                    .get()
                    .split(",")

                    if x.strip()

                ],

            "tags":

                [

                    x.strip()

                    for x in

                    self.form.tag_var
                    .get()
                    .split(",")

                    if x.strip()

                ],

            "answer":

                self.form.answer_text.get(
                    "1.0",
                    "end"
                ).strip()

        }

        self.storage.add(item)

        messagebox.showinfo(
            "Success",
            "Knowledge saved."
        )

        self.new()

        self.form.load_tree()

    # -----------------------------------------
    # Update
    # -----------------------------------------

    def update(self):

        if self.form.selected_id is None:

            messagebox.showwarning(
                "Warning",
                "Select an item."
            )

            return

        item = {

            "id": self.form.selected_id,

            "title":
                self.form.title_var.get(),

            "category":
                self.form.category_var.get(),

            "keywords":

                [

                    x.strip()

                    for x in

                    self.form.keyword_var
                    .get()
                    .split(",")

                    if x.strip()

                ],

            "tags":

                [

                    x.strip()

                    for x in

                    self.form.tag_var
                    .get()
                    .split(",")

                    if x.strip()

                ],

            "answer":

                self.form.answer_text.get(
                    "1.0",
                    "end"
                ).strip()

        }

        self.storage.update(item)

        messagebox.showinfo(
            "Success",
            "Knowledge updated."
        )

        self.form.load_tree()

    # -----------------------------------------
    # Delete
    # -----------------------------------------

    def delete(self):

        if self.form.selected_id is None:

            return

        confirm = messagebox.askyesno(

            "Delete",

            "Delete selected knowledge?"

        )

        if not confirm:

            return

        self.storage.delete(

            self.form.selected_id

        )

        self.new()

        self.form.load_tree()

    # -----------------------------------------
    # Smart Paste
    # -----------------------------------------

    def smart_paste(self):

        try:
            text = self.form.clipboard_get()
        except Exception:
            return

        if not text or not text.strip():
            return

        from core.smart_paste import SmartPaste

        sp = SmartPaste()
        parsed = sp.parse(text)

        if parsed.get("title"):
            self.form.title_var.set(parsed["title"])

        if parsed.get("category"):
            self.form.category_var.set(parsed["category"])

        if parsed.get("keywords"):
            self.form.keyword_var.set(", ".join(parsed["keywords"]))

        if parsed.get("tags"):
            self.form.tag_var.set(", ".join(parsed["tags"]))

        self.form.answer_text.delete(
            "1.0",
            "end"
        )

        self.form.answer_text.insert(
            "1.0",
            parsed["answer"]
        )