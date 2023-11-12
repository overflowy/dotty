import functools
from pathlib import Path

import rich
import yaml

from exceptions import DottyConfigException

CONFIG_FILENAME = "dotty.yml"
HOME_DIRECTORY = Path.home()
CONFIG_PATH = HOME_DIRECTORY / CONFIG_FILENAME


class DottyConfig:
    def save(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                yaml.safe_dump(self.data, f)
                rich.print("✅ [green]Saved config file at[/green]", str(CONFIG_PATH))
        except PermissionError:
            raise DottyConfigException(
                "❌ Cannot save config file. File might be in use by another process."
            )

    def load(self):
        try:
            with open(CONFIG_PATH) as f:
                self.data = yaml.safe_load(f)
                self.dotfiles_dir = Path(self.data["dotfiles_dir"])
                self.dotfiles = self.data["dotfiles"]
        except FileNotFoundError:
            raise DottyConfigException(
                "❌ Config file not found. Run 'dotty init' to create one."
            )
        except (yaml.YAMLError, KeyError):
            raise DottyConfigException(
                "❌ Invalid config file. Run 'dotty init' to create a new one."
            )

    def create(self, dotfiles_dir: str):
        self.data = {"dotfiles_dir": dotfiles_dir, "dotfiles": {}}
        self.save()


def with_config(func):
    @functools.wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):
        config = DottyConfig()
        return func(config, *args, **kwargs)

    return wrapper
