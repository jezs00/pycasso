#!/usr/bin/python3
# -*- coding:utf-8 -*-

import configparser
import os

from piblo.constants import ConfigConst, ProvidersConst, AutomaticConst
from piblo.file_operations import FileOperations


class Configs:
    """
    A class used to wrap config from a config file for pycasso.

    Attributes
    ----------

    Methods
    -------
    read_config(path)
        Retrieves config from provided relative path and applies to variables in this class. Returns ConfigParser
        object.

    init_config()
        Creates .config file from .config-example if

    write_config(configs, path) # Not yet implemented
        Writes config from a provided dict 'configs' to file at 'path'.

    set_config_terminal(path) # Not yet implemented
        Sets config file via terminal prompts
    """

    def __init__(self, path=os.getcwd(), config_path=ConfigConst.CONFIG_PATH.value,
                 example_config_path=ConfigConst.CONFIG_PATH_EG.value):
        # Paths
        self.file = FileOperations(path)

        self.config_path = self.file.get_full_path(config_path)
        self.example_path = self.file.get_full_path(example_config_path)

        # Set Defaults
        # File Settings
        self.save_image = ConfigConst.FILE_SAVE_IMAGE.value
        self.external_image_location = self.file.get_full_path(ConfigConst.FILE_EXTERNAL_IMAGE_LOCATION.value)
        self.generated_image_location = self.file.get_full_path(ConfigConst.FILE_GENERATED_IMAGE_LOCATION.value)
        self.image_format = ConfigConst.FILE_IMAGE_FORMAT.value
        self.font_file = self.file.get_full_path(ConfigConst.FILE_FONT_FILE.value)
        self.subjects_file = self.file.get_full_path(ConfigConst.FILE_SUBJECTS_FILE.value)
        self.artists_file = self.file.get_full_path(ConfigConst.FILE_ARTISTS_FILE.value)
        self.prompts_file = self.file.get_full_path(ConfigConst.FILE_PROMPTS_FILE.value)
        self.subjects_example = self.file.get_full_path(ConfigConst.FILE_SUBJECTS_EG.value)
        self.artists_example = self.file.get_full_path(ConfigConst.FILE_ARTISTS_EG.value)
        self.prompts_example = self.file.get_full_path(ConfigConst.FILE_PROMPTS_EG.value)
        self.resize_external = ConfigConst.FILE_RESIZE_EXTERNAL.value

        # Text Settings
        self.add_text = ConfigConst.TEXT_ADD_TEXT.value
        self.parse_file_text = ConfigConst.TEXT_PARSE_FILE_TEXT.value
        self.parse_random_text = ConfigConst.TEXT_PARSE_RANDOM_TEXT.value
        self.parse_brackets = ConfigConst.TEXT_PARSE_BRACKETS_LIST.value
        self.preamble_regex = ConfigConst.TEXT_PREAMBLE_REGEX.value
        self.artist_regex = ConfigConst.TEXT_ARTIST_REGEX.value
        self.remove_text = ConfigConst.TEXT_REMOVE_TEXT_LIST.value
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
        self.automatic_amount = ProvidersConst.AUTOMATIC_AMOUNT.value
        self.use_keychain = ProvidersConst.USE_KEYCHAIN.value
        self.credential_path = self.file.get_full_path(ProvidersConst.CREDENTIAL_PATH.value)
        self.test_enabled = ProvidersConst.TEST_ENABLED.value

        self.automatic_host = AutomaticConst.DEFAULT_HOST.value
        self.automatic_port = AutomaticConst.DEFAULT_PORT.value

        # Logging Settings
        self.log_file = ConfigConst.LOGGING_FILE.value
        self.log_level = ConfigConst.LOGGING_LEVEL.value

        # Generation Settings
        self.infill = ConfigConst.GENERATION_INFILL.value
        self.infill_percent = ConfigConst.GENERATION_INFILL_PERCENT.value

        # PiJuice Settings
        self.use_pijuice = ConfigConst.USE_PIJUICE.value
        self.shutdown_on_battery = ConfigConst.SHUTDOWN_ON_BATTERY.value
        self.shutdown_on_exception = ConfigConst.SHUTDOWN_ON_EXCEPTION.value
        self.wait_to_run = ConfigConst.WAIT_TO_RUN.value
        self.charge_display = ConfigConst.CHARGE_DISPLAY.value

        # Debug Settings
        self.test_epd_width = ConfigConst.TEST_EPD_WIDTH.value
        self.test_epd_height = ConfigConst.TEST_EPD_HEIGHT.value

        return

    def read_config(self):
        # Create new config file if necessary
        self.config_path = FileOperations.backup_file(self.config_path, self.example_path)

        # Method to read config file settings
        config = configparser.ConfigParser()
        config.read(self.config_path)

        if os.path.exists(self.config_path):

            # File Settings
            self.save_image = config.getboolean("File", "save_image", fallback=ConfigConst.FILE_SAVE_IMAGE.value)
            self.external_image_location = config.get("File", "external_image_location",
                                                      fallback=ConfigConst.FILE_EXTERNAL_IMAGE_LOCATION.value)
            self.generated_image_location = config.get("File", "generated_image_location",
                                                       fallback=ConfigConst.FILE_GENERATED_IMAGE_LOCATION.value)
            self.image_format = config.get("File", "image_format", fallback=ConfigConst.FILE_IMAGE_FORMAT.value)
            self.font_file = config.get("File", "font_file", fallback=ConfigConst.FILE_FONT_FILE.value)
            self.subjects_file = config.get("File", "subjects_file", fallback=ConfigConst.FILE_SUBJECTS_FILE.value)
            self.artists_file = config.get("File", "artists_file", fallback=ConfigConst.FILE_ARTISTS_FILE.value)
            self.prompts_file = config.get("File", "prompts_file", fallback=ConfigConst.FILE_PROMPTS_FILE.value)
            self.resize_external = config.getboolean("File", "resize_external",
                                                     fallback=ConfigConst.FILE_RESIZE_EXTERNAL.value)

            # Text Settings
            self.add_text = config.getboolean("Text", "add_text", fallback=ConfigConst.TEXT_ADD_TEXT.value)
            self.parse_file_text = config.getboolean("Text", "parse_file_text",
                                                     fallback=ConfigConst.TEXT_PARSE_FILE_TEXT.value)
            self.parse_random_text = config.getboolean("Text", "parse_random_text",
                                                       fallback=ConfigConst.TEXT_PARSE_RANDOM_TEXT.value)
            self.parse_brackets = []
            for text in config.get("Text", "parse_brackets",
                                   fallback=ConfigConst.TEXT_PARSE_BRACKETS.value).split("\n"):
                self.parse_brackets.append(text[1:-1])
            self.preamble_regex = config.get("Text", "preamble_regex",
                                             fallback=ConfigConst.TEXT_PREAMBLE_REGEX.value)[1:-1]
            self.artist_regex = config.get("Text", "artist_regex", fallback=ConfigConst.TEXT_ARTIST_REGEX.value)[1:-1]

            self.remove_text = []
            for text in config.get("Text", "remove_text", fallback=ConfigConst.TEXT_REMOVE_TEXT.value).split("\n"):
                self.remove_text.append(text[1:-1])

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
            self.prompt_preamble = config.get("Prompt", "preamble", fallback=ConfigConst.PROMPT_PREAMBLE.value)[1:-1]
            self.prompt_connector = config.get("Prompt", "connector", fallback=ConfigConst.PROMPT_CONNECTOR.value)[1:-1]
            self.prompt_postscript = config.get("Prompt", "postscript",
                                                fallback=ConfigConst.PROMPT_POSTSCRIPT.value)[1:-1]

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
            self.automatic_amount = config.getint("Providers", "automatic_amount",
                                                  fallback=ProvidersConst.AUTOMATIC_AMOUNT.value)
            self.use_keychain = config.getboolean("Providers", "use_keychain",
                                                  fallback=ProvidersConst.USE_KEYCHAIN.value)
            self.credential_path = config.get("Providers", "credential_path",
                                              fallback=ProvidersConst.CREDENTIAL_PATH.value)
            self.test_enabled = config.getboolean("Providers", "test_enabled",
                                                  fallback=ProvidersConst.TEST_ENABLED.value)

            self.automatic_host = config.get("Providers", "automatic_host",
                                             fallback=AutomaticConst.DEFAULT_HOST.value)
            self.automatic_host = config.getint("Providers", "automatic_port",
                                                fallback=AutomaticConst.DEFAULT_PORT.value)

            # Logging Settings
            self.log_file = config.get("Logging", "log_file", fallback=ConfigConst.LOGGING_FILE.value)
            self.log_level = config.getint("Logging", "log_level", fallback=ConfigConst.LOGGING_LEVEL.value)

            # Generation Settings
            self.infill = config.getboolean("Generation", "infill", fallback=ConfigConst.GENERATION_INFILL.value)
            self.infill_percent = config.getint("Generation", "infill_percent",
                                                fallback=ConfigConst.GENERATION_INFILL_PERCENT.value)

            # PiJuice Settings
            self.use_pijuice = config.getboolean("PiJuice", "use_pijuice", fallback=ConfigConst.USE_PIJUICE.value)
            self.shutdown_on_battery = config.getboolean("PiJuice", "shutdown_on_battery",
                                                         fallback=ConfigConst.SHUTDOWN_ON_BATTERY.value)
            self.shutdown_on_exception = config.getboolean("PiJuice", "shutdown_on_exception",
                                                           fallback=ConfigConst.SHUTDOWN_ON_EXCEPTION.value)
            self.wait_to_run = config.getint("PiJuice", "wait_to_run", fallback=ConfigConst.WAIT_TO_RUN.value)
            self.charge_display = config.getint("PiJuice", "charge_display", fallback=ConfigConst.CHARGE_DISPLAY.value)

            # Debug Settings
            self.test_epd_width = config.getint("Debug", "test_epd_width", fallback=ConfigConst.TEST_EPD_WIDTH.value)
            self.test_epd_height = config.getint("Debug", "test_epd_height", fallback=ConfigConst.TEST_EPD_HEIGHT.value)

            # Create new prompts if necessary and make them full paths
            self.subjects_file = self.file.get_full_path(self.subjects_file)
            self.artists_file = self.file.get_full_path(self.artists_file)
            self.prompts_file = self.file.get_full_path(self.prompts_file)

            self.subjects_file = FileOperations.backup_file(self.subjects_file, self.subjects_example)
            self.artists_file = FileOperations.backup_file(self.artists_file, self.artists_example)
            self.prompts_file = FileOperations.backup_file(self.prompts_file, self.prompts_example)

            # Set full paths for other paths
            self.external_image_location = self.file.get_full_path(self.external_image_location)
            self.generated_image_location = self.file.get_full_path(self.generated_image_location)
            self.font_file = self.file.get_full_path(self.font_file)
            self.credential_path = self.file.get_full_path(self.credential_path)

        return config

    def set_config_terminal(self, path):
        return
