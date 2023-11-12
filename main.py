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
