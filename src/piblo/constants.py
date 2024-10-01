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
    FILE_SAVE_IMAGE = True
    FILE_SAVE_DATE = True
    FILE_EXTERNAL_IMAGE_LOCATION = "images/external"
    FILE_GENERATED_IMAGE_LOCATION = "images/generated"
    FILE_IMAGE_FORMAT = "png"
    FILE_FONT_FILE = "resources/fonts/Font.ttc"
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
    TEXT_OVERRIDE_TEXT = False
    TEXT_OVERRIDE_PATH = "prompts/override.txt"

    # Icon Settings
    ICON_COLOR = "auto"
    ICON_PADDING = 10
    ICON_CORNER = "nw"
    ICON_SIZE = 20
    ICON_WIDTH = 3
    ICON_GAP = 5
    ICON_OPACITY = 150
    ICON_PATH = "resources/icons/"
    SHOW_BATTERY_ICON = True
    SHOW_PROVIDER_ICON = True
    SHOW_STATUS_ICON = True

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
    GENERATION_ROTATE = 0
    GENERATION_INFILL = False
    GENERATION_INFILL_PERCENT = 10

    # Post Settings
    POST_CONNECTOR = " in the style of "
    POST_TO_MASTODON = False
    MASTODON_APP_NAME = "new_app"
    MASTODON_BASE_URL = 'https://mastodon.social'
    MASTODON_CLIENT_CRED_PATH = "m_client.secret"
    MASTODON_USER_CRED_PATH = "m_user.secret"

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

    PROVIDER_FALLBACK = True

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
    DEFAULT_HOST = "https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image"
    MULTIPLE = 64


class AutomaticConst(Enum):
    HOST = "AUTOMATIC_HOST"
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 7860
    MULTIPLE = 8


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
    BAD = "BAD"
    WEAK = "WEAK"
    PRESENT = "PRESENT"


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
    FILE_TEST_TXT = "test_file.txt"
    CONFIG_FILE = ".testconfig"
    CONFIG_FOLDER = "test_config_wrapper_content"
    CONFIG_OLD_FILE = ".config-old"
    CONFIG_NEW_FILE = ".config-new"
    CONFIG_FAIL_FILE = ".does-not-exist"
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


class IconConst(Enum):
    LOC_TOP_LEFT = "nw"
    LOC_TOP_RIGHT = "ne"
    LOC_BOTTOM_LEFT = "sw"
    LOC_BOTTOM_RIGHT = "se"

    BACKGROUND_DARK_LIMIT = 127


class BatteryConst(Enum):
    ERROR = -1
    EMPTY = range(0, 20)
    LOW = range(21, 40)
    HALF = range(41, 60)
    GOOD = range(61, 80)
    FULL = range(81, 100)
    CHARGING = 101
    WEAK = 102
    BAD = -2


class IconFileConst(Enum):
    ICON_BATTERY_20 = ("battery.png", 10)
    ICON_BATTERY_40 = ("battery-1.png", 20)
    ICON_BATTERY_60 = ("battery-2.png", 30)
    ICON_BATTERY_80 = ("battery-3.png", 40)
    ICON_BATTERY_100 = ("battery-4.png", 50)
    ICON_BATTERY_ERROR = ("battery-off.png", 60)
    ICON_BATTERY_WEAK = ("battery-eco.png", 65)
    ICON_BATTERY_CHARGE = ("battery-charging-2.png", 70)

    ICON_TEST = ("stethoscope.png", 97)
    ICON_EXTERNAL = ("circle-letter-e.png", 100)
    ICON_HISTORIC = ("circle-letter-h.png", 110)
    ICON_STABLE = ("circle-letter-s.png", 120)
    ICON_DALLE = ("circle-letter-d.png", 130)
    ICON_AUTOMATIC = ("circle-letter-a.png", 140)

    ICON_TEST_FAIL = ("stethoscope-off.png", 67)
    ICON_EXTERNAL_FAIL = ("hexagon-letter-e.png", 70)
    ICON_HISTORIC_FAIL = ("hexagon-letter-h.png", 75)
    ICON_STABLE_FAIL = ("hexagon-letter-s.png", 80)
    ICON_DALLE_FAIL = ("hexagon-letter-d.png", 85)
    ICON_AUTOMATIC_FAIL = ("hexagon-letter-a.png", 90)

    ICON_EXCEPTION = ("heart-broken.png", 200)


class PosterConst(Enum):
    MASTODON = 1

    MASTODON_USER_KEYNAME = "MASTODON_USER"
    MASTODON_PASSWORD_KEYNAME = "MASTODON_PASSWORD"
    MASTODON_IMG_FORMAT = "PNG"
    MASTODON_MIME_FORMAT = "image/png"
