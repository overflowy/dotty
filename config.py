from pathlib import Path
from uuid import uuid4

import rich
import yaml
from rich.prompt import Prompt

from exceptions import DottyConfigException

CONFIG_FILENAME = "dotty.yml"
HOME_DIRECTORY = Path.home()
CONFIG_PATH = HOME_DIRECTORY / CONFIG_FILENAME


class DottyConfig:
    def save(self, print_msg=True):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                yaml.safe_dump(self.data, f, indent=2, sort_keys=False)
                if print_msg:
                    rich.print("✅ [green]Saved config file at[/green]", CONFIG_PATH)
        except PermissionError:
            raise DottyConfigException(
                "Cannot save config file. File might be in use by another process."
            )

    def load(self):
        try:
            with open(CONFIG_PATH) as f:
                self.data = yaml.safe_load(f)
                self.dotfiles_dir = Path(self.data["dotfiles_dir"])
                self.dotfiles = self.data["dotfiles"]
        except FileNotFoundError:
            raise DottyConfigException(
                "Config file not found. Run 'dotty init' to create one."
            )
        except (yaml.YAMLError, KeyError, TypeError):
            raise DottyConfigException(
                "Invalid config file. Run 'dotty init' to create a new one."
            )

    def create(self, dotfiles_dir: str):
        if CONFIG_PATH.exists():
            rich.print("❌ [red]A config file already exists[/red].")
            ok = Prompt.ask(
                "[blue]Do you want to overwrite it[/blue]?", choices=["y", "n"]
            )
            if ok != "y":
                exit(1)

        dotfiles_dir_path = Path(dotfiles_dir).resolve()

        if not dotfiles_dir_path.exists():
            rich.print("❌ [red]Dotfiles directory does not exist[/red].")
            ok = Prompt.ask(
                "[blue]Do you want to create it[/blue]?", choices=["y", "n"]
            )
            if ok == "y":
                dotfiles_dir_path.mkdir(parents=True)

        self.data = {"dotfiles_dir": dotfiles_dir_path.as_posix(), "dotfiles": {}}
        self.save()

    def add(self, dotfile: str):
        dotfile_path = Path(dotfile).resolve()
        short_uuid = str(uuid4())[:6]
        self.data["dotfiles"][dotfile_path.as_posix()] = short_uuid
        rich.print("✅ [green]Added dotfile[/green]:", dotfile_path.name)
        self.save(print_msg=False)

    def remove(self, dotfile_or_uid: str):
        pass
