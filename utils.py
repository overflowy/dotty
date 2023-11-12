from pathlib import Path

from config import CONFIG_FILENAME, HOME_DIRECTORY
from exceptions import DottyFileException


def validate_dotfile(dotfile: str) -> str:
    dotfile_path = Path(dotfile).resolve()
    if not dotfile_path.exists():
        raise DottyFileException("file does not exist")
    elif not dotfile_path.is_file():
        raise DottyFileException("not a file")
    elif HOME_DIRECTORY not in dotfile_path.parents:
        raise DottyFileException("file must be in the home directory")
    elif dotfile_path.name == CONFIG_FILENAME:
        raise DottyFileException("dotty's own config file cannot be added")
    return dotfile


def replace_home_with_dotfiles_dir(path: Path) -> Path:
    raise NotImplementedError
    # return Path(dotfiles_dir) / path.relative_to(HOME_DIRECTORY)


def replace_dotfiles_dir_with_home(path: Path) -> Path:
    raise NotImplementedError
    # return Path(HOME_DIRECTORY) / path.relative_to(dotfiles_dir)
