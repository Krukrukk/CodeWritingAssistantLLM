import configparser
import os
from pathlib import Path
import sys
from typing import Any


class Configuration:
    """
    Allows to read configuration file from script working directory.
    Configuration reading is done during objects initialization.
    """

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self.__read_config()

    def __read_config(self):
        """
        return config object containing the contents of the configuration file for script provided as init param
        """
        config = configparser.ConfigParser()
        config.optionxform = str
        try:
            config.read_file(open(self.config_file_path))
        except FileNotFoundError:
            print(
                f"Unable to load main configuration file with path {self.config_file_path}! Exiting."
            )
            sys.exit(1)
        return config

    def __getitem__(self, key):
        return self.config[key]

    def __setitem___(self, key, value):
        raise AttributeError("Cannot set a config value (read-only)")

    def __contains__(self, item):
        return item in self.config

    def get(self, key, value=None):
        if key in self.config:
            return self.config[key]
        elif value is not None:
            return value
        else:
            return None
