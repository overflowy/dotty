from typing import TypedDict
from pathlib import Path
from uuid import uuid4
import yaml
import rich

CONFIG_FILENAME = "dotty.yml"
HOME_DIRECTORY = Path.home()

CONFIG_PATH = HOME_DIRECTORY / CONFIG_FILENAME


class DottyConfig(TypedDict):
    dotfiles_dir: str
    dotfiles: list[dict[str, str]]


class DottyFileException(Exception):
    def __init__(self, file: str, message: str):
        super().__init__(message)
        rich.print("[red bold]ERROR[/red bold]: Cannot add file")
        rich.print(f"'[blue]{file}[/blue]' [[red]{message}[/red]]")
        exit(1)


def load_config(CONFIG_PATH: Path) -> DottyConfig:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config, f)


def get_short_uuid() -> str:
    return str(uuid4())[:5]


def validate_dotfile(dotfile: str):
    dotfile_path = Path(dotfile).resolve()
    if not dotfile_path.exists():
        raise DottyException(f"`{dotfile}` does not exist")
    elif not dotfile_path.is_file():
        raise DottyException(f"`{dotfile}` is not a file")
    elif HOME_DIRECTORY not in dotfile_path.parents:
        raise DottyException(f"`{dotfile}` is not in your home directory")
    elif dotfile_path.name == CONFIG_FILENAME:
        raise DottyException("dotty's config file cannot be added as a dotfile")
    return dotfile_path


def replace_home_with_dotfiles_dir(path: Path) -> Path:
    raise NotImplementedError
    # return Path(dotfiles_dir) / path.relative_to(HOME_DIRECTORY)


def replace_dotfiles_dir_with_home(path: Path) -> Path:
    raise NotImplementedError
    # return Path(HOME_DIRECTORY) / path.relative_to(dotfiles_dir)
