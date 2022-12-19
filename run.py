#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Python script to run pycasso - chooses between using pijuice or not based on config

from pycasso import Pycasso
import logging
import os
from constants import ConfigConst
from pijuice_handler import PiJuiceHandler

# Set up logging
file_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=ConfigConst.LOGGING_LEVEL, filename=os.path.join(file_path, ConfigConst.LOGGING_FILE))

instance = Pycasso()
if instance.config.use_pijuice:
    logging.info("Starting program using PiJuice")
    pijuice_instance = PiJuiceHandler()
    pijuice_instance.run()
    exit()
else:
    logging.info("Starting program without using PiJuice")
    instance.run()
    exit()
