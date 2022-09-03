# TODO: Unit tests
# TODO: option to allow custom height/width not matching epd

import configparser
from constants import ConfigConst


class Configs:
    """
    A class used to wrap config from a config file for pycasso.

    Attributes
    ----------

    Methods
    -------
    read_config(path)
        Retrieves config from provided path. Returns ConfigParser object.

    write_config(configs, path)
        Writes config from a provided dict 'configs' to file at 'path'.

    def set_config_terminal(path):
        Sets config file via terminal prompts
    """

    def __init__(self, path=ConfigConst.CONFIG_PATH.value):
        # TODO: Set up class to fully wrap config
        self.path = path
        return

    def read_config(self):
        # Method to read config file settings
        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def set_config_terminal(self, path):
        return
