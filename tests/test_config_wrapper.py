# Unit tests for config_wrapper.py
import os
from config_wrapper import Configs


def test_init():
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_config_wrapper_content/.testconfig')
    config = Configs(config_path)
    assert config.infill is False


def test_read_config():
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_config_wrapper_content/.testconfig')
    config = Configs(config_path)
    config.read_config()

    assert config.add_text is False
    assert config.infill is False
