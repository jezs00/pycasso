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
    FILE_RESIZE_EXTERNAL = True

    # Text Settings
    TEXT_ADD_TEXT = False
    TEXT_PARSE_FILE_TEXT = False
    TEXT_PARSE_RANDOM_TEXT = True
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
    GENERATION_INFILL = False
    GENERATION_INFILL_PERCENT = 10

    # PiJuice Settings
    USE_PIJUICE = False
    SHUTDOWN_ON_BATTERY = True
    SHUTDOWN_ON_EXCEPTION = False
    WAIT_TO_RUN = 30
    CHARGE_DISPLAY = 15

    # Debug Settings
    TEST_EPD_WIDTH = 500
    TEST_EPD_HEIGHT = 300


class ProvidersConst(Enum):
    # Settings and defaults for providers
    TEST = 99
    HISTORIC = 0
    EXTERNAL = 1
    STABLE = 2
    DALLE = 3
    MIDJOURNEY = 4
    AUTOMATIC = 5

    EXTERNAL_AMOUNT = 0
    HISTORIC_AMOUNT = 0
    STABLE_AMOUNT = 0
    DALLE_AMOUNT = 0
    AUTOMATIC_AMOUNT = 0

    USE_KEYCHAIN = False
    CREDENTIAL_PATH = ".creds"
    CREDENTIAL_PATH_EG = "examples/.creds-example"
    CREDENTIAL_SECTION = "Keys"

    TEST_ENABLED = True
    TEST_FILE = "examples/images/test.png"

    KEYCHAIN = "PYCASSO"
    STABLE_KEYNAME = "STABILITY"
    DALLE_KEYNAME = "DALLE"
    MIDJOURNEY_KEYNAME = "MIDJOURNEY"


class StabilityConst(Enum):
    KEY = "STABILITY_KEY"
    HOST = "STABILITY_HOST"
    DEFAULT_HOST = "grpc.stability.ai:443"
    MULTIPLE = 64


class AutomaticConst(Enum):
    HOST = "AUTOMATIC_HOST"
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 7860
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
    PYCASSO_CONFIG_RUN = ".config_run"
    PYCASSO_CONFIG_COMPLETE = ".config_complete"
    ARTISTS_FILE = "test_artists.txt"
    SUBJECTS_FILE = "test_subjects.txt"
    PROMPTS_FILE = "test_prompts.txt"
    FONT_FILE = "Font.ttc"
    PROVIDER_FOLDER = "test_provider_content"
    PROVIDER_CRED = ".creds-test"
    PROVIDER_CRED_NEW = ".creds-test-new"


class ImageConst(Enum):
    CONVERT_MODE = "RGB"
    DRAW_MODE = "RGBA"
    SUPPORTED_MODES = ["RGB", "RGBA"]


class EPDConst(Enum):
    COLOR = "color"
    BW = "bw"
    YELLOW = "yellow"
    RED = "red"
    PALETTE = "palette"
    FOUR_COLOR = "4color"
    FOUR_GRAY = "gray4"
