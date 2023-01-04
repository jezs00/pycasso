#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for config_wrapper.py

import os
from pycasso.config_wrapper import Configs
from pycasso.constants import UnitTestConst


def test_init():
    config_path = os.path.join(os.getcwd(), UnitTestConst.TEST_FOLDER.value, UnitTestConst.CONFIG_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    config = Configs(config_path)

    assert config.add_text is False
    assert config.infill is False


def test_read_config():
    config_path = os.path.join(os.getcwd(), UnitTestConst.TEST_FOLDER.value, UnitTestConst.CONFIG_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    config = Configs(config_path)
    config.read_config()

    assert config.add_text is False
    assert config.infill is False
