#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for config_wrapper.py

import os
from pycasso.config_wrapper import Configs
from pycasso.constants import TestConst


def test_init():
    config_path = os.path.join(os.getcwd(), TestConst.TEST_FOLDER.value, TestConst.CONFIG_FOLDER.value,
                               TestConst.CONFIG_FILE.value)
    config = Configs(config_path)

    assert config.add_text is False
    assert config.infill is False


def test_read_config():
    config_path = os.path.join(os.getcwd(), TestConst.TEST_FOLDER.value, TestConst.CONFIG_FOLDER.value,
                               TestConst.CONFIG_FILE.value)
    config = Configs(config_path)
    config.read_config()

    assert config.add_text is False
    assert config.infill is False
