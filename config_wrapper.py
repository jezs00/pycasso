# TODO: Unit tests
# TODO: option to allow custom height/width not matching epd

import configparser
import os

from constants import ConfigConst, ProvidersConst


class Configs:
    """
    A class used to wrap config from a config file for pycasso.

    Attributes
    ----------

    Methods
    -------
    read_config(path)
        Retrieves config from provided path and applies to variables in this class. Returns ConfigParser object.

    write_config(configs, path) # Not yet implemented
        Writes config from a provided dict 'configs' to file at 'path'.

    set_config_terminal(path) # Not yet implemented
        Sets config file via terminal prompts
    """

    def __init__(self, path=ConfigConst.CONFIG_PATH.value):
        self.path = path

        # Set Defaults
        # File Settings
        self.save_image = ConfigConst.FILE_SAVE_IMAGE.value
        self.external_image_location = ConfigConst.FILE_EXTERNAL_IMAGE_LOCATION.value
        self.generated_image_location = ConfigConst.FILE_GENERATED_IMAGE_LOCATION.value
        self.image_format = ConfigConst.FILE_IMAGE_FORMAT.value
        self.font_file = ConfigConst.FILE_FONT_FILE.value
        self.subjects_file = ConfigConst.FILE_SUBJECTS_FILE.value
        self.artists_file = ConfigConst.FILE_ARTISTS_FILE.value
        self.prompts_file = ConfigConst.FILE_PROMPTS_FILE.value

        # Text Settings
        self.add_text = ConfigConst.TEXT_ADD_TEXT.value
        self.parse_text = ConfigConst.TEXT_PARSE_TEXT.value
        self.preamble_regex = ConfigConst.TEXT_PREAMBLE_REGEX.value
        self.artist_regex = ConfigConst.TEXT_ARTIST_REGEX.value
        self.remove_text = ConfigConst.TEXT_REMOVE_TEXT.value
        self.box_to_floor = ConfigConst.TEXT_BOX_TO_FLOOR.value
        self.box_to_edge = ConfigConst.TEXT_BOX_TO_EDGE.value
        self.artist_loc = ConfigConst.TEXT_ARTIST_LOC.value
        self.artist_size = ConfigConst.TEXT_ARTIST_SIZE.value
        self.title_loc = ConfigConst.TEXT_TITLE_LOC.value
        self.title_size = ConfigConst.TEXT_TITLE_SIZE.value
        self.padding = ConfigConst.TEXT_PADDING.value
        self.opacity = ConfigConst.TEXT_OPACITY.value

        # Icon Settings
        self.icon_padding = ConfigConst.ICON_PADDING.value
        self.icon_size = ConfigConst.ICON_SIZE.value
        self.icon_width = ConfigConst.ICON_WIDTH.value
        self.icon_opacity = ConfigConst.ICON_OPACITY.value

        # Prompt Settings
        self.prompt_mode = ConfigConst.PROMPT_MODE.value
        self.prompt_preamble = ConfigConst.PROMPT_PREAMBLE.value
        self.prompt_connector = ConfigConst.PROMPT_CONNECTOR.value
        self.prompt_postscript = ConfigConst.PROMPT_POSTSCRIPT.value

        # Display Settings
        self.display_type = ConfigConst.DISPLAY_TYPE.value

        # Provider Settings
        self.external_amount = ProvidersConst.EXTERNAL_AMOUNT.value
        self.historic_amount = ProvidersConst.HISTORIC_AMOUNT.value
        self.stability_amount = ProvidersConst.STABLE_AMOUNT.value
        self.dalle_amount = ProvidersConst.DALLE_AMOUNT.value

        # Logging Settings
        self.log_file = ConfigConst.LOGGING_FILE.value
        self.log_level = ConfigConst.LOGGING_LEVEL.value

        # Generation Settings
        self.infill = ConfigConst.GENERATION_INFILL.value

        # PiJuice Settings
        self.shutdown_on_battery = ConfigConst.SHUTDOWN_ON_BATTERY.value
        self.wait_to_run = ConfigConst.WAIT_TO_RUN.value
        return

    def read_config(self):
        # Method to read config file settings
        config = configparser.ConfigParser()
        config.read(self.path)

        if os.path.exists(self.path):

            # File Settings
            self.save_image = config.getboolean("File", "save_image", fallback=ConfigConst.FILE_SAVE_IMAGE.value)
            self.external_image_location = config.get("File", "image_location",
                                                      fallback=ConfigConst.FILE_EXTERNAL_IMAGE_LOCATION.value)
            self.generated_image_location = config.get("File", "image_location",
                                                       fallback=ConfigConst.FILE_GENERATED_IMAGE_LOCATION.value)
            self.image_format = config.get("File", "image_format", fallback=ConfigConst.FILE_IMAGE_FORMAT.value)
            self.font_file = config.get("File", "font_file", fallback=ConfigConst.FILE_FONT_FILE.value)
            self.subjects_file = config.get("File", "subjects_file", fallback=ConfigConst.FILE_SUBJECTS_FILE.value)
            self.artists_file = config.get("File", "artists_file", fallback=ConfigConst.FILE_ARTISTS_FILE.value)
            self.prompts_file = config.get("File", "prompts_file", fallback=ConfigConst.FILE_PROMPTS_FILE.value)

            # Text Settings
            self.add_text = config.getboolean("Text", "add_text", fallback=ConfigConst.TEXT_ADD_TEXT.value)
            self.parse_text = config.getboolean("Text", "parse_text", fallback=ConfigConst.TEXT_PARSE_TEXT.value)
            self.preamble_regex = config.get("Text", "preamble_regex",
                                             fallback=ConfigConst.TEXT_PREAMBLE_REGEX.value)
            self.artist_regex = config.get("Text", "artist_regex", fallback=ConfigConst.TEXT_ARTIST_REGEX.value)
            self.remove_text = config.get("Text", "remove_text",
                                          fallback=ConfigConst.TEXT_REMOVE_TEXT.value).split("\n")
            self.box_to_floor = config.getboolean("Text", "box_to_floor",
                                                  fallback=ConfigConst.TEXT_BOX_TO_FLOOR.value)
            self.box_to_edge = config.getboolean("Text", "box_to_edge", fallback=ConfigConst.TEXT_BOX_TO_EDGE.value)
            self.artist_loc = config.getint("Text", "artist_loc", fallback=ConfigConst.TEXT_ARTIST_LOC.value)
            self.artist_size = config.getint("Text", "artist_size", fallback=ConfigConst.TEXT_ARTIST_SIZE.value)
            self.title_loc = config.getint("Text", "title_loc", fallback=ConfigConst.TEXT_TITLE_LOC.value)
            self.title_size = config.getint("Text", "title_size", fallback=ConfigConst.TEXT_TITLE_SIZE.value)
            self.padding = config.getint("Text", "padding", fallback=ConfigConst.TEXT_PADDING.value)
            self.opacity = config.getint("Text", "opacity", fallback=ConfigConst.TEXT_OPACITY.value)

            # Prompt
            self.prompt_mode = config.getint("Prompt", "mode", fallback=ConfigConst.PROMPT_MODE.value)

            # Icon
            self.icon_padding = config.getint("Icon", "icon_padding", fallback=ConfigConst.ICON_PADDING)
            self.icon_size = config.getint("Icon", "icon_size", fallback=ConfigConst.ICON_SIZE.value)
            self.icon_width = config.getint("Icon", "icon_width", fallback=ConfigConst.ICON_WIDTH.value)
            self.icon_opacity = config.getint("Icon", "icon_opacity", fallback=ConfigConst.ICON_OPACITY.value)

            # Display (rest of EPD config is just passed straight into displayfactory
            self.display_type = config.get("EPD", "type", fallback=ConfigConst.DISPLAY_TYPE.value)

            # Provider
            self.external_amount = config.getint("Providers", "external_amount",
                                                 fallback=ProvidersConst.EXTERNAL_AMOUNT.value)
            self.historic_amount = config.getint("Providers", "historic_amount",
                                                 fallback=ProvidersConst.HISTORIC_AMOUNT.value)
            self.stability_amount = config.getint("Providers", "stability_amount",
                                                  fallback=ProvidersConst.STABLE_AMOUNT.value)
            self.dalle_amount = config.getint("Providers", "dalle_amount",
                                              fallback=ProvidersConst.DALLE_AMOUNT.value)

            # Logging Settings
            self.log_file = config.get("Logging", "log_file", fallback=ConfigConst.LOGGING_FILE.value)
            self.log_level = config.getint("Logging", "log_level", fallback=ConfigConst.LOGGING_LEVEL.value)

            # Generation Settings
            self.infill = config.getboolean("Generation", "infill", fallback=ConfigConst.GENERATION_INFILL.value)

            # PiJuice Settings
            self.shutdown_on_battery = config.getboolean("PiJuice", "shutdown_on_battery",
                                                         fallback=ConfigConst.SHUTDOWN_ON_BATTERY.value)
            self.wait_to_run = config.getint("PiJuice", "wait_to_run", fallback=ConfigConst.WAIT_TO_RUN.value)

        return config

    def set_config_terminal(self, path):
        return
