#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
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
from file_operations import FileOperations
from constants import ProvidersConst, StabilityConst, ConfigConst, PropertiesConst, PromptMode
from provider import StabilityProvider, DalleProvider
from image_functions import ImageFunctions

lib_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib")
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)


# noinspection PyTypeChecker
class Pycasso:
    """
    Object used to run pycasso

    Attributes
    ----------

    Methods
    -------
    parse_args()
        Function parses arguments provided via command line. Sets internal args variable to argparser
        Also returns the argparser

    load_config()
        Loads config from file provided to it or sets defaults

    display_image_on_EPD(display_image, epd):
        Displays PIL image object 'display_image' on omni_epd object 'epd'

    run()
        Do pycasso
    """

    def __init__(self):
        self.file_path = os.path.dirname(os.path.abspath(__file__))

        # Config Dictionary for omni-epd
        self.config_dict = {}

        # Icon
        self.icon_shape = None

        # Keys
        self.stability_key = None
        self.dalle_key = None

        # Args read
        self.args = None
        self.parse_args()
        self.stability_key = self.args.stabilitykey
        self.dalle_key = self.args.dallekey
        if self.args.displayshape is not None:
            self.icon_shape = self.args.displayshape

        if self.args.savekeys:
            if self.stability_key is not None:
                StabilityProvider.add_secret(self.stability_key)
            if self.dalle_key is not None:
                DalleProvider.add_secret(self.dalle_key)

        # Load config or set defaults
        self.config = self.load_config()

        return

    def parse_args(self):
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
            parser.add_argument("--dallekey",
                                dest="dallekey",
                                type=str,
                                help="Dalle API Key")
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
            self.args = parser.parse_args()
        except argparse.ArgumentError as e:
            logging.error(e)
            exit()

        return self.args

    def load_config(self, config_path=None):
        # Loads config from file provided to it or sets defaults

        try:
            if config_path is None:
                config_path = ConfigConst.CONFIG_PATH.value
                if self.args is not None:
                    if self.args.configpath is not None:
                        config_path = self.args.configpath

            config = Configs(config_path)

            self.config_dict = config.read_config()

            # Set up logging
            if config.log_file is not None and config.log_file != "":
                log_file = os.path.join(self.file_path, config.log_file)

            logging.basicConfig(level=config.log_level, filename=log_file)
            logging.info("Config loaded")

        except IOError as e:
            logging.error(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            exit()

        return config

    @staticmethod
    def display_image_on_epd(display_image, epd):
        logging.info("Prepare epaper")
        epd.prepare()

        epd.display(display_image)

        logging.info("Send epaper to sleep")
        epd.close()
        return

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
        logging.info("pycasso has begun")

        try:
            epd = displayfactory.load_display_driver(self.config.display_type, self.config_dict)

        except EPDNotFoundError:
            logging.error(f"Couldn\'t find {self.config.display_type}")
            exit()

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            exit()

        if self.args.norun:
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
                self.config.external_amount,
                self.config.historic_amount,
                self.config.stability_amount,
                self.config.dalle_amount
            ))[0]

            artist_text = ""
            title_text = ""

            if provider_type == ProvidersConst.EXTERNAL.value:
                # External image load
                image_directory = os.path.join(self.file_path, self.config.external_image_location)
                if not os.path.exists(image_directory):
                    warnings.warn("External image directory path does not exist: '" + image_directory + "'")
                    exit()

                # Get random image from folder
                file = FileOperations(image_directory)
                image_path = file.get_random_file_of_type(self.config.image_format)
                image_base = Image.open(image_path)

                # Add text to via parsing if necessary
                image_name = os.path.basename(image_path)
                title_text = image_name

                if self.config.parse_text:
                    title_text, artist_text = FileOperations.get_title_and_artist(image_name,
                                                                                  self.config.preamble_regex,
                                                                                  self.config.artist_regex,
                                                                                  self.config.image_format)
                    title_text = FileOperations.remove_text(title_text, self.config.remove_text)
                    artist_text = FileOperations.remove_text(artist_text, self.config.remove_text)
                    title_text = title_text.title()
                    artist_text = artist_text.title()

                # Resize to thumbnail size based on epd resolution
                # TODO: allow users to choose between crop and resize
                epd_res = (epd.width, epd.height)
                image_base.thumbnail(epd_res)

            elif provider_type == ProvidersConst.HISTORIC.value:
                # Historic image previously saved
                image_directory = os.path.join(self.file_path, self.config.generated_image_location)
                if not os.path.exists(image_directory):
                    warnings.warn(f"Historic image directory path does not exist: '{image_directory}'")
                    exit()

                # Get random image from folder
                file = FileOperations(image_directory)
                image_path = file.get_random_file_of_type(self.config.image_format)
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
                prompt_mode = self.config.prompt_mode
                if prompt_mode == PromptMode.RANDOM.value:
                    # Pick random type of building
                    random.seed()
                    prompt_mode = random.randint(1, ConfigConst.PROMPT_MODES_COUNT.value)

                if prompt_mode == PromptMode.SUBJECT_ARTIST.value:
                    # Build prompt from artist/subject
                    artist_text = FileOperations.get_random_line(os.path.join(self.file_path, self.config.artists_file))
                    artist_text = FileOperations.parse_text(artist_text)
                    title_text = FileOperations.get_random_line(os.path.join(self.file_path, self.config.subjects_file))
                    title_text = FileOperations.parse_text(title_text)
                    prompt = (self.config.prompt_preamble + title_text + self.config.prompt_connector
                              + artist_text + self.config.prompt_postscript)
                    metadata.add_text(PropertiesConst.ARTIST.value, artist_text)
                    metadata.add_text(PropertiesConst.TITLE.value, title_text)

                elif prompt_mode == PromptMode.PROMPT.value:
                    # Build prompt from prompt file
                    title_text = FileOperations.get_random_line(os.path.join(self.file_path, self.config.prompts_file))
                    title_text = FileOperations.parse_text(title_text)
                    prompt = self.config.prompt_preamble + title_text + self.config.prompt_postscript
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
                    if self.stability_key is None:
                        stability_provider = StabilityProvider()
                    else:
                        stability_provider = StabilityProvider(key=self.stability_key)

                    logging.info("Getting Image")
                    fetch_height = ImageFunctions.ceiling_multiple(fetch_height, StabilityConst.MULTIPLE.value)
                    fetch_width = ImageFunctions.ceiling_multiple(fetch_width, StabilityConst.MULTIPLE.value)
                    image_base = stability_provider.get_image_from_string(prompt, fetch_height, fetch_width)

                elif provider_type == ProvidersConst.DALLE.value:
                    # Request image for Stability
                    logging.info("Loading Dalle API")
                    if self.dalle_key is None:
                        dalle_provider = DalleProvider()
                    else:
                        dalle_provider = DalleProvider(key=self.dalle_key)

                    logging.info("Getting Image")
                    image_base = dalle_provider.get_image_from_string(prompt, fetch_height, fetch_width)

                    # Use infill to fill in sides of image instead of cropping
                    if self.config.infill:
                        image_base = dalle_provider.infill_image_from_image(prompt, image_base)

                else:
                    # Invalid provider
                    warnings.warn(f"Invalid provider option chosen: {provider_type}")
                    exit()

                if self.config.save_image:
                    image_name = PropertiesConst.FILE_PREAMBLE.value + prompt + ".png"
                    save_path = os.path.join(self.file_path, self.config.generated_image_location, image_name)
                    logging.info(f"Saving image as {save_path}")

                    # Save the image
                    image_base.save(save_path, pnginfo=metadata)

            # Make sure image is correct size and centered after thumbnail set
            # Define locations and crop settings
            image_crop = ImageFunctions.get_crop_size(image_base.width, image_base.height, epd.width, epd.height)

            # Crop and prepare image
            image_base = image_base.crop(image_crop)
            draw = ImageDraw.Draw(image_base, "RGBA")

            # Draw status shape if provided
            if self.icon_shape is not None:
                draw = ImageFunctions.add_status_icon(draw, self.icon_shape, self.config.icon_padding,
                                                      self.config.icon_size, self.config.icon_width,
                                                      self.config.icon_opacity)

            # Draw text(s) if necessary
            if self.config.add_text:
                font_path = os.path.join(self.file_path, self.config.font_file)
                if not os.path.exists(font_path):
                    logging.info("Font file path does not exist: '" + self.config.font_file + "'")
                    exit()

                title_font = ImageFont.truetype(font_path, self.config.title_size)
                artist_font = ImageFont.truetype(font_path, self.config.artist_size)

                artist_box = (0, image_base.height, 0, image_base.height)
                title_box = artist_box

                if artist_text != "":
                    artist_box = draw.textbbox((epd.width / 2, image_base.height - self.config.artist_loc),
                                               artist_text, font=artist_font, anchor="mb")
                if title_text != "":
                    title_box = draw.textbbox((epd.width / 2, image_base.height - self.config.title_loc),
                                              title_text, font=title_font, anchor="mb")

                draw_box = ImageFunctions.max_area([artist_box, title_box])
                draw_box = tuple(numpy.add(draw_box, (-self.config.padding, -self.config.padding,
                                                      self.config.padding, self.config.padding)))

                # Modify depending on box type
                if self.config.box_to_floor:
                    draw_box = ImageFunctions.set_tuple_bottom(draw_box, image_base.height)

                if self.config.box_to_edge:
                    draw_box = ImageFunctions.set_tuple_sides(draw_box, -image_crop[0], image_crop[2])

                draw.rectangle(draw_box, fill=(255, 255, 255, self.config.opacity))
                draw.text((epd.width / 2, image_base.height - self.config.artist_loc), artist_text, font=artist_font,
                          anchor="mb", fill=0)
                draw.text((epd.width / 2, image_base.height - self.config.title_loc), title_text, font=title_font,
                          anchor="mb", fill=0)

            self.display_image_on_epd(image_base, epd)
            logging.shutdown()

        except EPDNotFoundError:
            warnings.warn(f"Couldn't find {self.config.display_type}")
            exit()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd.close()
            exit()
