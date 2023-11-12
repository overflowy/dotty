from pathlib import Path

import yaml

CONFIG_FILENAME = "dotty.yml"
HOME_DIRECTORY = Path.home()
DEFAULT_CONFIG_PATH = HOME_DIRECTORY / CONFIG_FILENAME


def load_config(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)
