import functools
from pathlib import Path
from typing import TypedDict

import yaml

CONFIG_FILENAME = "dotty.yml"
HOME_DIRECTORY = Path.home()
CONFIG_PATH = HOME_DIRECTORY / CONFIG_FILENAME


class DottyConfig(TypedDict):
    dotfiles_dir: str
    dotfiles: list[dict[str, str]]


def load_config(CONFIG_PATH: Path) -> DottyConfig:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f)


def with_config(func):
    @functools.wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):
        config = load_config(CONFIG_PATH)
        return func(config, *args, **kwargs)

    return wrapper
