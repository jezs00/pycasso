#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Python script to run pycasso - chooses between using pijuice or not based on config

from piblo.pycasso import Pycasso
from piblo.constants import ConfigConst
import logging
import os

# Set up logging
file_path = os.getcwd()
logging.basicConfig(level=ConfigConst.LOGGING_LEVEL.value,
                    filename=os.path.join(file_path, ConfigConst.LOGGING_FILE.value),
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

instance = Pycasso()
if instance.config.use_pijuice:
    from piblo.pijuice_handler import PiJuiceHandler

    logging.info("Starting program using PiJuice")
    pijuice_instance = PiJuiceHandler()
    pijuice_instance.run()
    exit()
else:
    logging.info("Starting program without using PiJuice")
    instance.run()
    exit()
