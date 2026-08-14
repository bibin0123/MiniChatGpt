import json
from pathlib import Path

from core.backup import BackupManager


class Storage:

    def __init__(self):

        self.json_file = Path("data/knowledge.json")
        self.txt_file = Path("data/knowledge.txt")

        self.backup = BackupManager()

    # -----------------------------------------
    # Load Knowledge
    # -----------------------------------------

    def load(self):

        if not self.json_file.exists():
            return []

        with open(
            self.json_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # -----------------------------------------
    # Save Knowledge
    # -----------------------------------------

    def save(self, data):

        with open(
            self.json_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        self.generate_text(data)

        self.backup.create_backup()

    # -----------------------------------------
    # Add Knowledge
    # -----------------------------------------

    def add(self, item):

        data = self.load()

        item["id"] = self.next_id(data)

        data.append(item)

        self.save(data)

        return item["id"]

    # -----------------------------------------
    # Update Knowledge
    # -----------------------------------------

    def update(self, item):

        data = self.load()

        for index, row in enumerate(data):

            if row["id"] == item["id"]:

                data[index] = item

                break

        self.save(data)

    # -----------------------------------------
    # Delete Knowledge
    # -----------------------------------------

    def delete(self, item_id):

        data = [

            row

            for row in self.load()

            if row["id"] != item_id

        ]

        self.save(data)

    # -----------------------------------------
    # Next ID
    # -----------------------------------------

    def next_id(self, data):

        if not data:
            return 1

        return max(

            row["id"]

            for row in data

        ) + 1

    # -----------------------------------------
    # Generate TXT
    # -----------------------------------------

    def generate_text(self, data):

        with open(
            self.txt_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "Knowledge Search Pro\n"
            )

            file.write("=" * 60)

            file.write("\n\n")

            for item in data:

                file.write(
                    f"Title : {item['title']}\n"
                )

                file.write(
                    f"Category : {item['category']}\n"
                )

                file.write(
                    "Keywords : "
                    + ", ".join(
                        item["keywords"]
                    )
                    + "\n"
                )

                if item.get("tags"):

                    file.write(
                        "Tags : "
                        + ", ".join(
                            item["tags"]
                        )
                        + "\n"
                    )

                file.write("\n")

                file.write(item["answer"])

                file.write("\n")

                file.write("-" * 60)

                file.write("\n\n")