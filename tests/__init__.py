import os
import piblo.constants

# Remove config file if it exists here
config_path = piblo.constants.ConfigConst.CONFIG_PATH.value

if os.path.exists(config_path):
    os.remove(config_path)
