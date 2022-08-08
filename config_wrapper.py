import configparser


# Method to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read('.config')
    return config
