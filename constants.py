# Enums for constants to be used throughout pycasso

from enum import Enum

import numpy


class ConfigConst(Enum):
    # Default settings that are loaded from config
    # Relative path to config
    DEFAULT_CONFIG_PATH = '.config'

    # Defaults
    # File Settings
    DEFAULT_IMAGE_LOCATION = 'images'
    DEFAULT_IMAGE_FORMAT = 'png'
    DEFAULT_FONT_FILE = 'fonts/Font.ttc'

    # Text Settings
    DEFAULT_ADD_TEXT = False
    DEFAULT_PARSE_TEXT = False
    DEFAULT_PREAMBLE_REGEX = '.*- '
    DEFAULT_ARTIST_REGEX = ' by '
    DEFAULT_REMOVE_TEXT = [", digital art", "A painting of"]
    DEFAULT_BOX_TO_FLOOR = True
    DEFAULT_BOX_TO_EDGE = True
    DEFAULT_ARTIST_LOC = 10
    DEFAULT_ARTIST_SIZE = 14
    DEFAULT_TITLE_LOC = 30
    DEFAULT_TITLE_SIZE = 20
    DEFAULT_PADDING = 10
    DEFAULT_OPACITY = 150

    # Display Settings
    DEFAULT_DISPLAY_TYPE = 'omni_epd.mock'

    # Debug Settings
    DEFAULT_IMAGE_VIEWER = False


class ProvidersConst(Enum):
    # Settings and defaults for providers
    HISTORIC = 0
    STABLE = 1
    DALLE = 2
    MIDJOURNEY = 3

    HISTORIC_AMOUNT = 1
    STABLE_AMOUNT = 0
    DALLE_AMOUNT = 0
    MIDJOURNEY_AMOUNT = 0

    KEYCHAIN = "PYCASSO"
    STABLE_KEYNAME = "STABILITY"
    DALLE_KEYNAME = "DALLE"
    MIDJOURNEY_KEYNAME = "MIDJOURNEY"


class StabilityConst(Enum):
    KEY = "STABILITY_KEY"
    HOST = "STABILITY_HOST"
    DEFAULT_HOST = "grpc.stability.ai:443"
