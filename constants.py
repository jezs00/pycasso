# Enums for constants to be used throughout pycasso

from enum import Enum

import numpy


class ConfigConst(Enum):
    # Default settings that are loaded from config
    # Relative path to config
    CONFIG_PATH = '.config'

    # Defaults
    # File Settings
    FILE_SAVE_IMAGE = 1
    FILE_IMAGE_LOCATION = 'images'
    FILE_IMAGE_FORMAT = 'png'
    FILE_FONT_FILE = 'fonts/Font.ttc'
    FILE_SUBJECTS_FILE = 'prompts/subjects.txt'
    FILE_ARTISTS_FILE = 'prompts/artists.txt'
    FILE_PROMPTS_FILE = 'prompts/prompts.txt'

    # Text Settings
    TEXT_ADD_TEXT = False
    TEXT_PARSE_TEXT = False
    TEXT_PREAMBLE_REGEX = '.*- '
    TEXT_ARTIST_REGEX = ' by '
    TEXT_REMOVE_TEXT = [", digital art", "A painting of"]
    TEXT_BOX_TO_FLOOR = True
    TEXT_BOX_TO_EDGE = True
    TEXT_ARTIST_LOC = 10
    TEXT_ARTIST_SIZE = 14
    TEXT_TITLE_LOC = 30
    TEXT_TITLE_SIZE = 20
    TEXT_PADDING = 10
    TEXT_OPACITY = 150

    # Automatic prompt construction
    PROMPT_MODES_COUNT = 2
    PROMPT_MODE = 1
    PROMPT_PREAMBLE = ''
    PROMPT_CONNECTOR = ' by '
    PROMPT_POSTSCRIPT = ', digital art, trending on artstation'

    # Display Settings
    DISPLAY_TYPE = 'omni_epd.mock'

    # Debug Settings
    DEBUG_IMAGE_VIEWER = False


class ProvidersConst(Enum):
    # Settings and defaults for providers
    HISTORIC = 0
    STABLE = 1
    DALLE = 2
    MIDJOURNEY = 3

    HISTORIC_AMOUNT = 1
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
