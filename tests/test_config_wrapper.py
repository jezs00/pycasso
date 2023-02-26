#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for config_wrapper.py
import glob
import os
from piblo.config_wrapper import Configs
from piblo.constants import UnitTestConst


def test_init():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    config = Configs(config_path)

    assert config.add_text is False
    assert config.infill is False


def test_read_config():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    config = Configs(config_path)
    config.read_config()

    assert config.add_text is False
    assert config.infill is False


def test_insert_config():
    config_old_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                                   UnitTestConst.CONFIG_OLD_FILE.value)
    config_new_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                                   UnitTestConst.CONFIG_NEW_FILE.value)
    old_config = Configs(config_path=config_old_path)
    new_config = Configs(config_path=config_new_path)

    old_config.config.read(config_old_path)
    old_config.load_config(old_config.config)

    old_config.insert_config(new_config.read_config())
    old_config.load_config(old_config.config)

    assert old_config.prompt_connector == "OLD CONNECTOR"
    assert old_config.prompt_postscript == "POSTSCRIPT WAS MISSING"


def test_write_config():
    config_old_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                                   UnitTestConst.CONFIG_OLD_FILE.value)
    config_new_path = os.path.join(os.path.dirname(__file__), UnitTestConst.TEMP_FOLDER.value,
                                   UnitTestConst.CONFIG_FILE.value)

    # Cleanup files before
    if os.path.exists(config_new_path):
        os.remove(config_new_path)

    old_config = Configs(config_path=config_old_path)
    old_config.config.read(config_old_path)
    old_config.load_config(old_config.config)
    old_config.write_config(config_new_path)

    new_config = Configs(config_path=config_new_path)
    new_config.read_config()

    assert os.path.exists(config_new_path)
    assert new_config.prompt_connector == "OLD CONNECTOR"

    # Cleanup files after
    if os.path.exists(config_new_path):
        os.remove(config_new_path)


def test_does_config_file_exist():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                               UnitTestConst.CONFIG_FILE.value)
    config = Configs(config_path=config_path)
    assert config.does_config_file_exist()


def test_does_config_file_exist_not():
    config_path = os.path.join(os.path.dirname(__file__), UnitTestConst.CONFIG_FOLDER.value,
                               UnitTestConst.CONFIG_FAIL_FILE.value)
    config = Configs(config_path=config_path)
    assert not config.does_config_file_exist()


def test_read_string():
    s = "\"STRING WITH QUOTES\""
    expected = "STRING WITH QUOTES"
    result = Configs.read_string(s)
    assert result == expected


def test_read_string_half_quotes():
    s = "\"STRING WITH 1 QUOTE"
    expected = "\"STRING WITH 1 QUOTE"
    result = Configs.read_string(s)
    assert result == expected


def test_read_string_no_quotes():
    s = "STRING WITHOUT QUOTES"
    expected = "STRING WITHOUT QUOTES"
    result = Configs.read_string(s)
    assert result == expected
