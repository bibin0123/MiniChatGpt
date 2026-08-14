import json
from pathlib import Path
from shutil import copy2
from datetime import datetime


class BackupManager:

    def __init__(self):

        self.data_folder = Path("data")
        self.backup_folder = Path("backups")
        self.config_file = Path("data/config.json")

        self.backup_folder.mkdir(exist_ok=True)

    # -----------------------------------------
    # Get Max Backups from Config
    # -----------------------------------------

    def get_max_backups(self):

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("max_backups", 1)
            except Exception:
                pass

        return 1

    # -----------------------------------------
    # Create Backup
    # -----------------------------------------

    def create_backup(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for file in self.data_folder.iterdir():

            if file.is_file():

                backup_name = (
                    f"{file.stem}_{timestamp}"
                    f"{file.suffix}"
                )

                copy2(
                    file,
                    self.backup_folder / backup_name
                )

        max_keep = self.get_max_backups()
        self.cleanup(keep=max_keep)

    # -----------------------------------------
    # Remove Old Backups
    # -----------------------------------------

    def cleanup(self, keep=1):

        if not self.backup_folder.exists():
            return

        groups = {}

        for file in self.backup_folder.iterdir():

            if file.is_file():

                # Extract base prefix (e.g. 'knowledge' from 'knowledge_20260803_180312.json')
                parts = file.stem.split("_")
                prefix = parts[0] if parts else file.stem
                group_key = (prefix, file.suffix)

                groups.setdefault(group_key, []).append(file)

        for key, file_list in groups.items():

            file_list.sort(
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )

            for file in file_list[keep:]:
                try:
                    file.unlink()
                except Exception:
                    pass

    # -----------------------------------------
    # Backup Count
    # -----------------------------------------

    def count(self):

        return len(
            list(
                self.backup_folder.iterdir()
            )
        )