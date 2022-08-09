import configparser


# Method to read config file settings
def read_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config
