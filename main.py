from config import DottyConfig
from utils import validate_dotfile


def init(dotfiles_dir: str, config=DottyConfig()):
    config.create(dotfiles_dir)


def add(dotfile: str, config=DottyConfig()):
    dotfile = validate_dotfile(dotfile)
    config.load()
    config.add(dotfile)
