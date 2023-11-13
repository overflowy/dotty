from enum import Enum
from pathlib import Path
from shutil import copy2
from typing import NamedTuple

import rich
from rich.console import Console
from rich.table import Table

from config import CONFIG_FILENAME, HOME_DIRECTORY, DottyConfig
from exceptions import DottyFileException


def validate_dotfile(dotfile: str, dotfiles_path: Path) -> str:
    dotfile_path = Path(dotfile).resolve()
    if not dotfile_path.exists():
        raise DottyFileException("file does not exist.")
    elif not dotfile_path.is_file():
        raise DottyFileException("not a file.")
    elif HOME_DIRECTORY not in dotfile_path.parents:
        raise DottyFileException("file must be in the home directory.")
    elif dotfile_path in dotfiles_path.parents:
        raise DottyFileException("file must not be in the dotfiles directory.")
    elif dotfile_path.name == CONFIG_FILENAME:
        raise DottyFileException("dotty's own config file cannot be added.")
    return dotfile


class FileAction(Enum):
    NOTHING = "✅ Nothing"
    BACK_UP = "💾 Back up"
    RESTORE = "🔄 Restore"
    NOT_FOUND = "❌ Not found"


class FileCopyInstruction(NamedTuple):
    src: Path
    dst: Path


class SyncUtil:
    def __init__(self, config=DottyConfig()):
        self.config = config
        self.config.load()
        self.dotfiles_dir = self.config.dotfiles_dir
        self.copy_instructions: list[FileCopyInstruction] = []

    def _init_report_table(self):
        self.table = Table()
        self.table.add_column("Action", no_wrap=True)
        self.table.add_column("File", style="magenta", overflow="fold")
        self.table.add_column("Dir", style="cyan", overflow="ellipsis")
        self.table.add_column("Size", justify="right", style="green")

    def _to_readable_size(self, size: int) -> str:
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024 ** 2:.2f} MB"
        else:
            return f"{size / 1024 ** 3:.2f} GB"

    def _add_row(self, action: FileAction, file_path: Path):
        try:
            readable_size = self._to_readable_size(file_path.stat().st_size)
        except FileNotFoundError:
            readable_size = ""

        self.table.add_row(
            action.value, file_path.name, str(file_path.parent.name), readable_size
        )

    def print_report(self):
        console = Console()
        console.print(self.table)

    def prepare_sync(self):
        self._init_report_table()

        for dotfile in self.config.dotfiles:
            dotfile_path = Path(dotfile)
            backup_path = self._to_backup_path(dotfile_path)
            if paths := self._diff_paths(dotfile_path, backup_path):
                self.copy_instructions.append(paths)

        self.print_report()

    def sync(self):
        if self.copy_instructions:
            rich.print("📂 [blue]Copying files[/blue]...")
        for instr in self.copy_instructions:
            instr.dst.parent.mkdir(parents=True, exist_ok=True)
            copy2(instr.src, instr.dst)

    def _to_backup_path(self, dotfile_path: Path) -> Path:
        return self.dotfiles_dir / dotfile_path.relative_to(HOME_DIRECTORY)

    def _to_original_path(self, dotfile_path: Path) -> Path:
        return Path(HOME_DIRECTORY) / dotfile_path.relative_to(self.dotfiles_dir)

    def _handle_dotfile_not_exists(
        self, dotfile_path: Path, backup_path: Path
    ) -> FileCopyInstruction | None:
        if not backup_path.exists():
            self._add_row(FileAction.NOT_FOUND, dotfile_path)
            return None
        else:
            self._add_row(FileAction.RESTORE, dotfile_path)
            return FileCopyInstruction(src=backup_path, dst=dotfile_path)

    def _handle_backup_not_exists(
        self, dotfile_path: Path, backup_path: Path
    ) -> FileCopyInstruction:
        self._add_row(FileAction.BACK_UP, dotfile_path)
        return FileCopyInstruction(src=dotfile_path, dst=backup_path)

    def _compare_file_modification_times(
        self, dotfile_path: Path, backup_path: Path
    ) -> FileCopyInstruction | None:
        dotfile_mtime = dotfile_path.stat().st_mtime
        backup_mtime = backup_path.stat().st_mtime

        if dotfile_mtime > backup_mtime:
            self._add_row(FileAction.BACK_UP, dotfile_path)
            return FileCopyInstruction(src=dotfile_path, dst=backup_path)

        elif dotfile_mtime < backup_mtime:
            self._add_row(FileAction.RESTORE, dotfile_path)
            return FileCopyInstruction(src=backup_path, dst=dotfile_path)

        else:
            self._add_row(FileAction.NOTHING, dotfile_path)
            return None

    def _diff_paths(
        self, dotfile_path: Path, backup_path: Path
    ) -> FileCopyInstruction | None:
        if not dotfile_path.exists():
            return self._handle_dotfile_not_exists(dotfile_path, backup_path)

        if not backup_path.exists():
            return self._handle_backup_not_exists(dotfile_path, backup_path)

        return self._compare_file_modification_times(dotfile_path, backup_path)
