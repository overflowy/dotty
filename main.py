from pathlib import Path
from shutil import copy2

import rich

from config import DottyConfig
from file_utils import (
    FileCopyInstruction,
    diff_paths,
    to_backup_path,
    validate_dotfile,
)


def init(dotfiles_dir: str, config=DottyConfig()):
    config.create(dotfiles_dir)


def add(dotfile: str, config=DottyConfig()):
    config.load()
    dotfile = validate_dotfile(dotfile, dotfiles_path=config.dotfiles_dir)
    config.load()
    config.add(dotfile)


def sync(dry_run: bool = False, config=DottyConfig()):
    rich.print("🔄 [blue]Syncing dotfiles[/blue]...")

    copy_instructions: list[FileCopyInstruction] = []
    config.load()

    for dotfile in config.dotfiles:
        dotfile_path = Path(dotfile)
        backup_path = to_backup_path(dotfile_path, config.dotfiles_dir)
        if paths := diff_paths(dotfile_path, backup_path):
            copy_instructions.append(paths)

    if dry_run:
        return

    if copy_instructions:
        rich.print("📂 [blue]Copying files[/blue]...")
    for instr in copy_instructions:
        instr.dst.parent.mkdir(parents=True, exist_ok=True)
        copy2(instr.src, instr.dst)

    rich.print("✅ [green]All dotfiles are up to date[/green].")
