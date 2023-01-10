import os
import sys
import piblo.constants

# Remove config file if it exists here
config_path = piblo.constants.ConfigConst.CONFIG_PATH.value

# Import path for github tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

if os.path.exists(config_path):
    os.remove(config_path)
