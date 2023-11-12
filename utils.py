from pathlib import Path
from uuid import uuid4

from config import CONFIG_FILENAME, HOME_DIRECTORY
from exceptions import DottyFileException


def get_short_uuid() -> str:
    return str(uuid4())[:5]


def validate_dotfile(dotfile: str):
    dotfile_path = Path(dotfile).resolve()
    if not dotfile_path.exists():
        raise DottyFileException(dotfile, "file does not exist")
    elif not dotfile_path.is_file():
        raise DottyFileException(dotfile, "not a file")
    elif HOME_DIRECTORY not in dotfile_path.parents:
        raise DottyFileException(dotfile, "file must be in the home directory")
    elif dotfile_path.name == CONFIG_FILENAME:
        raise DottyFileException(dotfile, "dotty's config file cannot be added")
    return dotfile_path


def replace_home_with_dotfiles_dir(path: Path) -> Path:
    raise NotImplementedError
    # return Path(dotfiles_dir) / path.relative_to(HOME_DIRECTORY)


def replace_dotfiles_dir_with_home(path: Path) -> Path:
    raise NotImplementedError
    # return Path(HOME_DIRECTORY) / path.relative_to(dotfiles_dir)
