from pathlib import Path

from config import CONFIG_FILENAME, HOME_DIRECTORY
from exceptions import DottyFileException


def validate_dotfile(dotfile: str, dotfiles_path: Path) -> str:
    dotfile_path = Path(dotfile).resolve()
    if not dotfile_path.exists():
        raise DottyFileException("file does not exist")
    elif not dotfile_path.is_file():
        raise DottyFileException("not a file")
    elif HOME_DIRECTORY not in dotfile_path.parents:
        raise DottyFileException("file must be in the home directory")
    elif dotfile_path in dotfiles_path.parents:
        raise DottyFileException("file must not be in the dotfiles directory")
    elif dotfile_path.name == CONFIG_FILENAME:
        raise DottyFileException("dotty's own config file cannot be added")
    return dotfile


def to_backup_path(dotfile: Path, dotfiles_dir: Path) -> Path:
    return dotfiles_dir / dotfile.relative_to(HOME_DIRECTORY)


def to_original_path(dotfile: Path, dotfiles_dir: Path) -> Path:
    return Path(HOME_DIRECTORY) / dotfile.relative_to(dotfiles_dir)
