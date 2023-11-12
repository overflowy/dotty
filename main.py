from pathlib import Path
from typing import TypedDict
from uuid import uuid4

import yaml


class DottyConfig(TypedDict):
    dotfiles_dir: str
    dotfiles: list[dict[str, str]]


CONFIG_FILENAME = "dotty.yml"
HOME_DIRECTORY = Path.home()
DEFAULT_CONFIG_PATH = HOME_DIRECTORY / CONFIG_FILENAME


def load_config(config_path: str) -> DottyConfig:
    with open(config_path) as f:
        return yaml.safe_load(f)


def save_config(config, config_path: str):
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)
def get_short_uuid() -> str:
    return str(uuid4())[:5]
def check_dotfile(dotfile: str) -> str | None:
    error_msg = None


def check_dotfile(dotfile: str) -> Path | None:
    error_msg = None
    dotfile_path = Path(dotfile).resolve()
    if not dotfile_path.exists():
        error_msg = f"'{dotfile}' does not exist"
    elif not dotfile_path.is_file():
        error_msg = f"'{dotfile}' is not a file"
    elif HOME_DIRECTORY not in dotfile_path.parents:
        error_msg = f"'{dotfile}' is not in your home directory"
    elif dotfile_path.name == CONFIG_FILENAME:
        error_msg = "You can't add dotty's config file to your dotfiles"
    if error_msg:
        print(error_msg)
        return None
    return dotfile_path
