import rich

from config import DottyConfig
from file_utils import SyncUtil, validate_dotfile


def init(dotfiles_dir: str, config=DottyConfig()):
    config.create(dotfiles_dir)


def add(dotfile: str, config=DottyConfig()):
    config.load()
    dotfile = validate_dotfile(dotfile, dotfiles_path=config.dotfiles_dir)
    config.load()
    config.add(dotfile)


def sync(dry_run: bool = False):
    rich.print("💫 [blue]Syncing files[/blue]...")
    sync_util = SyncUtil()
    sync_util.prepare_sync()

    if dry_run:
        rich.print("✅ [yellow]No changes made[/yellow].")
        return

    sync_util.sync()
