#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Enums for constants to be used throughout pycasso

import logging
from enum import Enum


class ConfigConst(Enum):
    # Default settings that are loaded from config
    # Relative path to config
    CONFIG_PATH = ".config"
    CONFIG_PATH_EG = "examples/.config-example"

    # Defaults
    # File Settings
    FILE_SAVE_IMAGE = 1
    FILE_EXTERNAL_IMAGE_LOCATION = "images/external"
    FILE_GENERATED_IMAGE_LOCATION = "images/generated"
    FILE_IMAGE_FORMAT = "png"
    FILE_FONT_FILE = "fonts/Font.ttc"
    FILE_SUBJECTS_FILE = "prompts/subjects.txt"
    FILE_ARTISTS_FILE = "prompts/artists.txt"
    FILE_PROMPTS_FILE = "prompts/prompts.txt"
    FILE_SUBJECTS_EG = "examples/prompts/subjects-example.txt"
    FILE_ARTISTS_EG = "examples/prompts/artists-example.txt"
    FILE_PROMPTS_EG = "examples/prompts/prompts-example.txt"

    # Text Settings
    TEXT_ADD_TEXT = False
    TEXT_PARSE_TEXT = False
    TEXT_PARSE_BRACKETS = "\"()\"\n\"[]\"\n\"{}\""
    TEXT_PARSE_BRACKETS_LIST = ["()", "[]", "{}"]
    TEXT_PREAMBLE_REGEX = ".*- "
    TEXT_ARTIST_REGEX = " by "
    TEXT_REMOVE_TEXT = "\"()\"\n\"[]\"\n\"{}\""
    TEXT_REMOVE_TEXT_LIST = [", digital art", "A painting of"]
    TEXT_BOX_TO_FLOOR = True
    TEXT_BOX_TO_EDGE = True
    TEXT_ARTIST_LOC = 10
    TEXT_ARTIST_SIZE = 14
    TEXT_TITLE_LOC = 30
    TEXT_TITLE_SIZE = 20
    TEXT_PADDING = 10
    TEXT_OPACITY = 150

    # Icon Settings
    ICON_PADDING = 10
    ICON_SIZE = 20
    ICON_WIDTH = 3
    ICON_OPACITY = 150

    # Automatic Prompt Construction Settings
    PROMPT_MODES_COUNT = 2
    PROMPT_MODE = 1
    PROMPT_PREAMBLE = ""
    PROMPT_CONNECTOR = " by "
    PROMPT_POSTSCRIPT = ", digital art, trending on artstation"

    # Display Settings
    DISPLAY_TYPE = "omni_epd.mock"

    # Logging Settings
    LOGGING_FILE = "pycasso.log"
    LOGGING_LEVEL = logging.DEBUG

    # Generation Settings
    GENERATION_INFILL = 0

    # PiJuice Settings
    USE_PIJUICE = False
    SHUTDOWN_ON_BATTERY = True
    WAIT_TO_RUN = 30
    CHARGE_DISPLAY = 15


class ProvidersConst(Enum):
    # Settings and defaults for providers
    HISTORIC = 0
    EXTERNAL = 1
    STABLE = 2
    DALLE = 3
    MIDJOURNEY = 4

    EXTERNAL_AMOUNT = 1
    HISTORIC_AMOUNT = 0
    STABLE_AMOUNT = 0
    DALLE_AMOUNT = 0

    KEYCHAIN = "PYCASSO"
    STABLE_KEYNAME = "STABILITY"
    DALLE_KEYNAME = "DALLE"
    MIDJOURNEY_KEYNAME = "MIDJOURNEY"


class StabilityConst(Enum):
    KEY = "STABILITY_KEY"
    HOST = "STABILITY_HOST"
    DEFAULT_HOST = "grpc.stability.ai:443"
    MULTIPLE = 64


class DalleConst(Enum):
    SIZES = {
        256: "256x256",
        512: "512x512",
        1024: "1024x1024"
    }


class PiJuiceConst(Enum):
    STATUS_ROOT = "data"
    STATUS_POWER = "powerInput"

    NOT_PRESENT = "NOT_PRESENT"


class PropertiesConst(Enum):
    FILE_PREAMBLE = "pycasso - "
    ARTIST = "artist"
    TITLE = "title"
    PROMPT = "prompt"


class PromptModeConst(Enum):
    RANDOM = 0
    SUBJECT_ARTIST = 1
    PROMPT = 2


class DisplayShapeConst(Enum):
    SQUARE = 0
    CROSS = 1
    TRIANGLE = 2
    CIRCLE = 3


class UnitTestConst(Enum):
    TEST_FOLDER = "tests/"
    FILE_OPERATIONS_FOLDER = "test_file_operations_content"
    CONFIG_FILE = ".testconfig"
    CONFIG_FOLDER = "test_config_wrapper_content"
    TEMP_FOLDER = "test_temp"
    PYCASSO_FOLDER = "test_pycasso_content"
    ARTISTS_FILE = "artists.txt"
    SUBJECTS_FILE = "subjects.txt"
    PROMPTS_FILE = "prompts.txt"
    FONT_FILE = "Font.ttc"
