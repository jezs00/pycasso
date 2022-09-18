#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import random
import warnings
import argparse
import numpy
import logging

from config_wrapper import Configs
from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from file_loader import FileLoader
from constants import ProvidersConst, StabilityConst, ConfigConst, PropertiesConst, PromptMode
from provider import StabilityProvider

lib_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib")
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)


class Pycasso:
    """
    Object used to run pycasso

    Attributes
    ----------

    Methods
    -------
    run()
        Do pycasso

    max_area(area_list)
        Takes an array of tuples and returns the largest area within them
        (a, b, c, d) - will return the smallest value for a,b and largest value for c,d

    set_tuple_bottom(tup, bottom)
        Helper to set fourth element in four element tuple
        In context of application, sets the bottom coordinate of the box

    set_tuple_sides(tup, left, right)
        Helper to set first and third element in four element tuple
        In context of application, sets the left and right coordinates of the box

    ceiling_multiple(number, multiple)
        Helper to find next multiple of 'multiple' for number
    """

    def __init__(self):
        self.file_path = os.path.dirname(os.path.abspath(__file__))

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

        # Prompt
        self.prompt_mode = ConfigConst.PROMPT_MODE.value
        self.preamble = ConfigConst.PROMPT_PREAMBLE.value
        self.connector = ConfigConst.PROMPT_CONNECTOR.value
        self.postscript = ConfigConst.PROMPT_POSTSCRIPT.value

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

        # Keys
        self.stability_key = None

        # Draw
        self.display_shape = None
        return

    @staticmethod
    def max_area(area_list):
        # initialise
        a, b, c, d = area_list[0]

        # find max for each element
        for t in area_list:
            at, bt, ct, dt = t
            a = min(a, at)
            b = min(b, bt)
            c = max(c, ct)
            d = max(d, dt)
        tup = (a, b, c, d)
        return tup

    @staticmethod
    def set_tuple_bottom(tup, bottom):
        a, b, c, d = tup
        tup = (a, b, c, bottom)
        return tup

    @staticmethod
    def set_tuple_sides(tup, left, right):
        a, b, c, d = tup
        tup = (left, b, right, d)
        return tup

    @staticmethod
    def ceiling_multiple(number, multiple):
        return int(multiple * numpy.ceil(number / multiple))

    # TODO: Functions to run to clean up switching the modes
    def load_historic_image(self):
        return

    def load_stability_image(self):
        return

    def load_dalle_image(self):
        return

    def load_historic_text(self):
        return

    def prep_prompt_text(self):
        return

    def run(self):
        try:
            parser = argparse.ArgumentParser(
                description="A program to request an image from preset APIs and apply them to an"
                            " epaper screen through a raspberry pi unit")
            parser.add_argument("--configpath",
                                dest="configpath",
                                type=str,
                                help="Path to .config file. Default: \'.config\'")
            parser.add_argument("--stabilitykey",
                                dest="stabilitykey",
                                type=str,
                                help="Stable Diffusion API Key")
            parser.add_argument("--savekeys",
                                dest="savekeys",
                                action="store_const",
                                const=1,
                                default=0,
                                help="Use this flag to save any keys provided to system keyring")
            parser.add_argument("--norun",
                                dest="norun",
                                action="store_const",
                                const=1,
                                default=0,
                                help="This flag ends the program before starting the main functionality of pycasso. This will "
                                     "not fetch images or update the epaper screen")
            parser.add_argument("--displayshape",
                                dest="displayshape",
                                type=int,
                                help="Displays a shape in the top left corner of the epd. Good for providing visual information"
                                     " while using a mostly disconnected headless setup."
                                     "\n0 - Square\n1 - Cross\n2 - Triangle\n3 - Circle")
            args = parser.parse_args()
            stability_key = args.stabilitykey
            display_shape = args.displayshape

            if args.savekeys:
                if stability_key is not None:
                    StabilityProvider.add_secret(stability_key)

        except argparse.ArgumentError as e:
            logging.error(e)
            exit()

        # TODO: pull this out and put into config_wrapper.py
        config = {}

        try:
            if args.configpath is None:
                config_load = Configs(os.path.join(self.file_path, ConfigConst.CONFIG_PATH.value))
            else:
                config_load = Configs(args.configpath)

            # Load config
            if os.path.exists(config_load.path):
                config = config_load.read_config()

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
                self.preamble = config.get("Prompt", "preamble", fallback=ConfigConst.PROMPT_PREAMBLE.value)
                self.connector = config.get("Prompt", "connector", fallback=ConfigConst.PROMPT_CONNECTOR.value)
                self.postscript = config.get("Prompt", "postscript", fallback=ConfigConst.PROMPT_POSTSCRIPT.value)

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

            # Set up logging
            if self.log_file is not None and self.log_file != "":
                self.log_file = os.path.join(self.file_path, self.log_file)

            logging.basicConfig(level=self.log_level, filename=self.log_file)
            logging.info("Config loaded")

        except IOError as e:
            logging.error(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            exit()

        logging.info("pycasso has begun")

        try:
            epd = displayfactory.load_display_driver(self.display_type, config)

        except EPDNotFoundError:
            logging.error(f"Couldn\'t find {self.display_type}")
            exit()

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            exit()

        if args.norun:
            logging.info("--norun option used, closing pycasso without running")
            exit()

        try:
            # Build list
            provider_types = [
                ProvidersConst.EXTERNAL.value,
                ProvidersConst.HISTORIC.value,
                ProvidersConst.STABLE.value,
                ProvidersConst.DALLE.value
            ]

            # Pick random provider based on weight
            random.seed()
            provider_type = random.choices(provider_types, k=1, weights=(
                self.external_amount,
                self.historic_amount,
                self.stability_amount,
                self.dalle_amount
            ))[0]

            # TODO: Code starting to look a little spaghetti. Clean up once API works.

            artist_text = ""
            title_text = ""

            if provider_type == ProvidersConst.EXTERNAL.value:
                # External image load
                image_directory = os.path.join(self.file_path, self.external_image_location)
                if not os.path.exists(image_directory):
                    warnings.warn("External image directory path does not exist: '" + image_directory + "'")
                    exit()

                # Get random image from folder
                file = FileLoader(image_directory)
                image_path = file.get_random_file_of_type(self.image_format)
                image_base = Image.open(image_path)

                # Add text to via parsing if necessary
                image_name = os.path.basename(image_path)
                title_text = image_name

                if self.parse_text:
                    title_text, artist_text = FileLoader.get_title_and_artist(image_name,
                                                                              self.preamble_regex, self.artist_regex,
                                                                              self.image_format)
                    title_text = FileLoader.remove_text(title_text, self.remove_text)
                    artist_text = FileLoader.remove_text(artist_text, self.remove_text)
                    title_text = title_text.title()
                    artist_text = artist_text.title()

                # Resize to thumbnail size based on epd resolution
                # TODO: allow users to choose between crop and resize
                epd_res = (epd.width, epd.height)
                image_base.thumbnail(epd_res)

            elif provider_type == ProvidersConst.HISTORIC.value:
                # Historic image previously saved
                image_directory = os.path.join(self.file_path, self.generated_image_location)
                if not os.path.exists(image_directory):
                    warnings.warn(f"Historic image directory path does not exist: '{image_directory}'")
                    exit()

                # Get random image from folder
                file = FileLoader(image_directory)
                image_path = file.get_random_file_of_type(self.image_format)
                image_base = Image.open(image_path)
                image_name = os.path.basename(image_path)
                title_text = image_name

                # Get and apply metadata if it exists
                metadata = image_base.text
                if PropertiesConst.TITLE.value in metadata.keys():
                    title_text = metadata[PropertiesConst.TITLE.value]
                elif PropertiesConst.PROMPT.value in metadata.keys():
                    title_text = metadata[PropertiesConst.PROMPT.value]
                if PropertiesConst.ARTIST.value in metadata.keys():
                    artist_text = metadata[PropertiesConst.ARTIST.value]

            else:
                # Build prompt, add metadata as we go
                metadata = PngImagePlugin.PngInfo()
                if self.prompt_mode == PromptMode.RANDOM.value:
                    # Pick random type of building
                    random.seed()
                    prompt_mode = random.randint(1, ConfigConst.PROMPT_MODES_COUNT.value)

                if prompt_mode == PromptMode.SUBJECT_ARTIST.value:
                    # Build prompt from artist/subject
                    artist_text = FileLoader.get_random_line(os.path.join(self.file_path, self.artists_file))
                    title_text = FileLoader.get_random_line(os.path.join(self.file_path, self.subjects_file))
                    prompt = self.preamble + title_text + " " + self.connector + " " + artist_text + self.postscript
                    metadata.add_text(PropertiesConst.ARTIST.value, artist_text)
                    metadata.add_text(PropertiesConst.TITLE.value, title_text)

                elif prompt_mode == PromptMode.PROMPT.value:
                    # Build prompt from prompt file
                    title_text = FileLoader.get_random_line(os.path.join(self.file_path, self.prompts_file))
                    prompt = self.preamble + title_text + self.postscript
                else:
                    warnings.warn("Invalid prompt mode chosen. Exiting application.")
                    exit()

                metadata.add_text(PropertiesConst.PROMPT.value, prompt)
                fetch_height = epd.height
                fetch_width = epd.width

                logging.info(f"Requesting \'{prompt}\'")

                # Pick between providers
                if provider_type == ProvidersConst.STABLE.value:
                    # Request image for Stability
                    logging.info("Loading Stability API")
                    if stability_key is None:
                        stability_provider = StabilityProvider()
                    else:
                        stability_provider = StabilityProvider(key=stability_key)

                    logging.info("Getting Image")
                    fetch_height = Pycasso.ceiling_multiple(epd.height, StabilityConst.MULTIPLE.value)
                    fetch_width = Pycasso.ceiling_multiple(epd.width, StabilityConst.MULTIPLE.value)
                    image_base = stability_provider.get_image_from_string(prompt, fetch_height, fetch_width)

                elif provider_type == ProvidersConst.DALLE.value:
                    # Request image for DALLE
                    warnings.warn("DALLE not yet implemented. Exiting application.")
                    exit()

                else:
                    # Invalid provider
                    warnings.warn(f"Invalid provider option chosen: {provider_type}")
                    exit()

                if self.save_image:
                    image_name = prompt + ".png"
                    save_path = os.path.join(self.file_path, self.generated_image_location, image_name)
                    logging.info(f"Saving image as {save_path}")

                    # Save the image
                    image_base.save(save_path, pnginfo=metadata)

            # Make sure image is correct size and centered after thumbnail set
            # Define locations and crop settings
            width_diff = (epd.width - image_base.width) / 2
            height_diff = (epd.height - image_base.height) / 2
            left_pixel = 0 - width_diff
            top_pixel = 0 - height_diff
            right_pixel = image_base.width + width_diff
            bottom_pixel = image_base.height + height_diff
            image_crop = (left_pixel, top_pixel, right_pixel, bottom_pixel)

            # Crop and prepare image
            image_base = image_base.crop(image_crop)
            draw = ImageDraw.Draw(image_base, "RGBA")

            # Draw status shape if provided
            if display_shape is not None:
                # Make bounding box
                status_padding = 5
                status_size = 10  # TODO: put in config
                status_width = 3
                status_opacity = 150
                status_corner = status_padding + status_size
                status_box = (status_padding, status_padding, status_corner, status_corner)
                status_circle = (status_padding + status_size / 2, status_padding + status_size / 2, status_size / 2)
                if display_shape == 1:
                    draw.rectangle(status_box,
                                   width=0,
                                   fill=(0, 0, 0, status_opacity))
                    draw.line(status_box,
                              width=status_width,
                              fill=(255, 255, 255, status_opacity))
                    status_box = (status_corner, status_padding, status_padding, status_corner)
                    draw.line(status_box,
                              width=status_width,
                              fill=(255, 255, 255, status_opacity))
                elif display_shape == 2:
                    # TODO: triangle doesn't have line thickness and lines overlap
                    draw.regular_polygon(status_circle,
                                         n_sides=3,
                                         fill=(0, 0, 0, status_opacity),
                                         outline=(255, 255, 255, status_opacity))
                elif display_shape == 3:
                    draw.ellipse(status_box,
                                 width=status_width,
                                 fill=(0, 0, 0, status_opacity),
                                 outline=(255, 255, 255, status_opacity))
                else:
                    draw.rectangle(status_box,
                                   width=status_width,
                                   fill=(0, 0, 0, status_opacity),
                                   outline=(255, 255, 255, status_opacity))

            # Draw text(s) if necessary
            if self.add_text:
                # TODO: bottom box doesn't look great if image crops with black space on the top and bottom
                # TODO: some special characters break font
                font_path = os.path.join(self.file_path, self.font_file)
                if not os.path.exists(font_path):
                    logging.info("Font file path does not exist: '" + self.font_file + "'")
                    exit()

                title_font = ImageFont.truetype(font_path, self.title_size)
                artist_font = ImageFont.truetype(font_path, self.artist_size)

                artist_box = (0, epd.height, 0, epd.height)
                title_box = artist_box
                if artist_text != "":
                    artist_box = draw.textbbox((epd.width / 2, epd.height - self.artist_loc),
                                               artist_text, font=artist_font, anchor="mb")
                if title_text != "":
                    title_box = draw.textbbox((epd.width / 2, epd.height - self.title_loc),
                                              title_text, font=title_font, anchor="mb")

                draw_box = Pycasso.max_area([artist_box, title_box])
                draw_box = tuple(numpy.add(draw_box, (-self.padding, -self.padding, self.padding, self.padding)))

                # Modify depending on box type
                if self.box_to_floor:
                    draw_box = Pycasso.set_tuple_bottom(draw_box, bottom_pixel)

                if self.box_to_edge:
                    draw_box = Pycasso.set_tuple_sides(draw_box, width_diff, right_pixel)

                draw.rectangle(draw_box, fill=(255, 255, 255, self.opacity))
                draw.text((epd.width / 2, epd.height - self.artist_loc), artist_text, font=artist_font, anchor="mb",
                          fill=0)
                draw.text((epd.width / 2, epd.height - self.title_loc), title_text, font=title_font, anchor="mb",
                          fill=0)

            logging.info("Prepare epaper")
            epd.prepare()

            epd.display(image_base)

            logging.info("Send epaper to sleep")
            epd.close()
            logging.shutdown()

        except EPDNotFoundError:
            logging.info(f"Couldn't find {self.display_type}")
            exit()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd.close()
            exit()


instance = Pycasso()
instance.run()
