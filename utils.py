from pathlib import Path
from typing import NamedTuple

import rich

from config import CONFIG_FILENAME, HOME_DIRECTORY
from exceptions import DottyFileException


class FileCopyInstruction(NamedTuple):
    src: Path
    dst: Path


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


def to_backup_path(dotfile_path: Path, dotfiles_dir: Path) -> Path:
    return dotfiles_dir / dotfile_path.relative_to(HOME_DIRECTORY)


def to_original_path(dotfile_path: Path, dotfiles_dir: Path) -> Path:
    return Path(HOME_DIRECTORY) / dotfile_path.relative_to(dotfiles_dir)


def handle_dotfile_not_exists(
    dotfile_path: Path, backup_path: Path
) -> FileCopyInstruction | None:
    if not backup_path.exists():
        rich.print(
            f"❌ [yellow]'{dotfile_path}' not found (stale entry?)[/yellow], skipping"
        )
        return None
    else:
        rich.print(f"🔹 '{dotfile_path}' not found, preparing to restore")
        return FileCopyInstruction(src=backup_path, dst=dotfile_path)


def handle_backup_not_exists(
    dotfile_path: Path, backup_path: Path
) -> FileCopyInstruction:
    rich.print(f"🔹 '{dotfile_path}' is not backed up, preparing to back up")
    return FileCopyInstruction(src=dotfile_path, dst=backup_path)


def compare_file_modification_times(
    dotfile_path: Path, backup_path: Path
) -> FileCopyInstruction | None:
    dotfile_mtime = dotfile_path.stat().st_mtime
    backup_mtime = backup_path.stat().st_mtime

    if dotfile_mtime > backup_mtime:
        rich.print(f"🔹 '{dotfile_path}' is newer, preparing to back up")
        return FileCopyInstruction(src=dotfile_path, dst=backup_path)

    elif dotfile_mtime < backup_mtime:
        rich.print(f"🔹 '{dotfile_path}' is older, preparing to restore")
        return FileCopyInstruction(src=backup_path, dst=dotfile_path)

    else:
        rich.print(f"🔹 '{dotfile_path}' is up to date, skipping")
        return None


def compare_paths(dotfile_path: Path, backup_path: Path) -> FileCopyInstruction | None:
    if not dotfile_path.exists():
        return handle_dotfile_not_exists(dotfile_path, backup_path)

    if not backup_path.exists():
        return handle_backup_not_exists(dotfile_path, backup_path)

    return compare_file_modification_times(dotfile_path, backup_path)
