from pathlib import Path
from shutil import copy2

import rich

from config import DottyConfig
from utils import to_backup_path, validate_dotfile


def init(dotfiles_dir: str, config=DottyConfig()):
    config.create(dotfiles_dir)


def add(dotfile: str, config=DottyConfig()):
    dotfile = validate_dotfile(dotfile)
    config.load()
    config.add(dotfile)


def sync(dry_run: bool = False, config=DottyConfig()):
    to_copy: list[tuple[Path, Path]] = []

    config.load()
    for dotfile in config.dotfiles:
        dotfile = Path(dotfile)
        backup = to_backup_path(dotfile, config.dotfiles_dir)
        if not backup.exists():
            to_copy.append((dotfile, backup))
        else:
            dotfile_mtime = dotfile.stat().st_mtime
            backup_mtime = backup.stat().st_mtime
            if backup_mtime < dotfile_mtime:
                to_copy.append((dotfile, backup))
            else:
                to_copy.append((backup, dotfile))

    if dry_run:
        return

    for src, dst in to_copy:
        dst.parent.mkdir(parents=True, exist_ok=True)
        copy2(src, dst)
