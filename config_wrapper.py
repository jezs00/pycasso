import configparser
from constants import ConfigConst


# Method to read config file settings

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

    def __init__(self, path=ConfigConst.DEFAULT_CONFIG_PATH.value):
        #TODO: Set up class to fully wrap config
        self.path = path
        return

    def read_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def set_config_terminal(self, path):
        return
