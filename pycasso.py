#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import random
import warnings
import argparse

import numpy

import logging

from numpy import ceil

from config_wrapper import Configs
from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image, ImageDraw, ImageFont
from file_loader import FileLoader
from constants import ProvidersConst, StabilityConst, ConfigConst
from provider import StabilityProvider

lib_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)


# Takes an array of tuples and returns the largest area within them
# (a, b, c, d) - will return the smallest value for a,b and largest value for c,d
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


# Helper to set fourth element in four element tuple
# In context of application, sets the bottom coordinate of the box
def set_tuple_bottom(tup, bottom):
    a, b, c, d = tup
    tup = (a, b, c, bottom)
    return tup


# Helper to set first and third element in four element tuple
# In context of application, sets the left and right coordinates of the box
def set_tuple_sides(tup, left, right):
    a, b, c, d = tup
    tup = (left, b, right, d)
    return tup


# Helper to find next multiple of 'multiple' for number
def ceiling_multiple(number, multiple):
    return int(multiple * ceil(number / multiple))


# TODO: Functions to run to clean up switching the modes
def load_historic_image():
    return


def load_stability_image():
    return


def load_dalle_image():
    return


def load_historic_text():
    return


def prep_prompt_text():
    return


# Set Defaults
# File Settings
save_image = ConfigConst.FILE_SAVE_IMAGE.value
image_location = ConfigConst.FILE_IMAGE_LOCATION.value
image_format = ConfigConst.FILE_IMAGE_FORMAT.value
font_file = ConfigConst.FILE_FONT_FILE.value
subjects_file = ConfigConst.FILE_SUBJECTS_FILE.value
artists_file = ConfigConst.FILE_ARTISTS_FILE.value
prompts_file = ConfigConst.FILE_PROMPTS_FILE.value

# Text Settings
add_text = ConfigConst.TEXT_ADD_TEXT.value
parse_text = ConfigConst.TEXT_PARSE_TEXT.value
preamble_regex = ConfigConst.TEXT_PREAMBLE_REGEX.value
artist_regex = ConfigConst.TEXT_ARTIST_REGEX.value
remove_text = ConfigConst.TEXT_REMOVE_TEXT.value
box_to_floor = ConfigConst.TEXT_BOX_TO_FLOOR.value
box_to_edge = ConfigConst.TEXT_BOX_TO_EDGE.value
artist_loc = ConfigConst.TEXT_ARTIST_LOC.value
artist_size = ConfigConst.TEXT_ARTIST_SIZE.value
title_loc = ConfigConst.TEXT_TITLE_LOC.value
title_size = ConfigConst.TEXT_TITLE_SIZE.value
padding = ConfigConst.TEXT_PADDING.value
opacity = ConfigConst.TEXT_OPACITY.value

# Prompt
prompt_mode = ConfigConst.PROMPT_MODE.value
preamble = ConfigConst.PROMPT_PREAMBLE.value
connector = ConfigConst.PROMPT_CONNECTOR.value
postscript = ConfigConst.PROMPT_POSTSCRIPT.value

# Display Settings
display_type = ConfigConst.DISPLAY_TYPE.value

# Provider Settings
historic_amount = ProvidersConst.HISTORIC_AMOUNT.value
stability_amount = ProvidersConst.STABLE_AMOUNT.value
dalle_amount = ProvidersConst.DALLE_AMOUNT.value

# Logging Settings
log_file = ConfigConst.LOGGING_FILE.value
log_level = ConfigConst.LOGGING_LEVEL.value

# Keys
stability_key = None

# Draw
display_shape = None

filepath = os.path.dirname(os.path.abspath(__file__))

try:
    parser = argparse.ArgumentParser(description='A program to request an image from preset APIs and apply them to an'
                                                 ' epaper screen through a raspberry pi unit')
    parser.add_argument('--configpath',
                        dest='configpath',
                        type=str,
                        help='Path to .config file. Default: \'.config\'')
    parser.add_argument('--stabilitykey',
                        dest='stabilitykey',
                        type=str,
                        help='Stable Diffusion API Key')
    parser.add_argument('--savekeys',
                        dest='savekeys',
                        action='store_const',
                        const=1,
                        default=0,
                        help='Use this flag to save any keys provided to system keyring')
    parser.add_argument('--norun',
                        dest='norun',
                        action='store_const',
                        const=1,
                        default=0,
                        help='This flag ends the program before starting the main functionality of pycasso. This will '
                             'not fetch images or update the epaper screen')
    parser.add_argument('--displayshape',
                        dest='displayshape',
                        type=int,
                        help='Displays a shape in the top left corner of the epd. Good for providing visual information'
                             ' while using a mostly disconnected headless setup.'
                             '\n0 - Square\n1 - Cross\n2 - Triangle\n3 - Circle')
    args = parser.parse_args()
    stability_key = args.stabilitykey
    display_shape = args.displayshape

    if args.savekeys:
        if stability_key is not None:
            StabilityProvider.add_secret(stability_key)

except argparse.ArgumentError as e:
    logging.error(e)

# TODO: pull this out and put into config_wrapper.py
config = {}

try:
    if args.configpath is None:
        config_load = Configs(filepath + '/' + ConfigConst.CONFIG_PATH.value)
    else:
        config_load = Configs(args.configpath)

    # Load config
    if os.path.exists(config_load.path):
        config = config_load.read_config()

        # File Settings
        save_image = config.getboolean('File', 'save_image', fallback=ConfigConst.FILE_SAVE_IMAGE.value)
        image_location = config.get('File', 'image_location', fallback=ConfigConst.FILE_IMAGE_LOCATION.value)
        image_format = config.get('File', 'image_format', fallback=ConfigConst.FILE_IMAGE_LOCATION.value)
        font_file = config.get('File', 'font_file', fallback=ConfigConst.FILE_FONT_FILE.value)
        subjects_file = config.get('File', 'subjects_file', fallback=ConfigConst.FILE_SUBJECTS_FILE.value)
        artists_file = config.get('File', 'artists_file', fallback=ConfigConst.FILE_ARTISTS_FILE.value)
        prompts_file = config.get('File', 'prompts_file', fallback=ConfigConst.FILE_PROMPTS_FILE.value)

        # Text Settings
        add_text = config.getboolean('Text', 'add_text', fallback=ConfigConst.TEXT_ADD_TEXT.value)
        parse_text = config.getboolean('Text', 'parse_text', fallback=ConfigConst.TEXT_PARSE_TEXT.value)
        preamble_regex = config.get('Text', 'preamble_regex', fallback=ConfigConst.TEXT_PREAMBLE_REGEX.value)
        artist_regex = config.get('Text', 'artist_regex', fallback=ConfigConst.TEXT_ARTIST_REGEX.value)
        remove_text = config.get('Text', 'remove_text', fallback=ConfigConst.TEXT_REMOVE_TEXT.value).split('\n')
        box_to_floor = config.getboolean('Text', 'box_to_floor', fallback=ConfigConst.TEXT_BOX_TO_FLOOR.value)
        box_to_edge = config.getboolean('Text', 'box_to_edge', fallback=ConfigConst.TEXT_BOX_TO_EDGE.value)
        artist_loc = config.getint('Text', 'artist_loc', fallback=ConfigConst.TEXT_ARTIST_LOC.value)
        artist_size = config.getint('Text', 'artist_size', fallback=ConfigConst.TEXT_ARTIST_SIZE.value)
        title_loc = config.getint('Text', 'title_loc', fallback=ConfigConst.TEXT_TITLE_LOC.value)
        title_size = config.getint('Text', 'title_size', fallback=ConfigConst.TEXT_TITLE_SIZE.value)
        padding = config.getint('Text', 'padding', fallback=ConfigConst.TEXT_PADDING.value)
        opacity = config.getint('Text', 'opacity', fallback=ConfigConst.TEXT_OPACITY.value)

        # Prompt
        prompt_mode = config.getint('Prompt', 'mode', fallback=ConfigConst.PROMPT_MODE.value)
        preamble = config.get('Prompt', 'preamble', fallback=ConfigConst.PROMPT_PREAMBLE.value)
        connector = config.get('Prompt', 'connector', fallback=ConfigConst.PROMPT_CONNECTOR.value)
        postscript = config.get('Prompt', 'postscript', fallback=ConfigConst.PROMPT_POSTSCRIPT.value)

        # Display (rest of EPD config is just passed straight into displayfactory
        display_type = config.get('EPD', 'type', fallback=ConfigConst.DISPLAY_TYPE.value)

        # Provider
        historic_amount = config.getint('Providers', 'historic_amount', fallback=ProvidersConst.HISTORIC_AMOUNT.value)
        stability_amount = config.getint('Providers', 'stability_amount', fallback=ProvidersConst.STABLE_AMOUNT.value)
        dalle_amount = config.getint('Providers', 'dalle_amount', fallback=ProvidersConst.DALLE_AMOUNT.value)

        # Logging Settings
        log_file = config.get('Logging', 'log_file', fallback=ConfigConst.LOGGING_FILE.value)
        log_level = config.getint('Logging', 'log_level', fallback=ConfigConst.LOGGING_LEVEL.value)

    # Set up logging
    if log_file is not None and log_file != "":
        log_file = filepath + '/' + log_file

    logging.basicConfig(level=log_level, filename=log_file)
    logging.info("Config loaded")

except IOError as e:
    logging.error(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

logging.info("pycasso has begun")

try:
    epd = displayfactory.load_display_driver(display_type, config)

except EPDNotFoundError:
    logging.error(f"Couldn't find {display_type}")
    exit()

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

if args.norun:
    logging.info("--norun option used, closing pycasso without running")
    exit()

try:
    # TODO: set up different image loaders - one for internal and one for external
    # Build list
    provider_types = [
        ProvidersConst.HISTORIC.value,
        ProvidersConst.STABLE.value,
        ProvidersConst.DALLE.value
    ]

    # Pick random provider based on weight
    random.seed()
    provider_type = random.choices(provider_types, k=1, weights=(
        historic_amount,
        stability_amount,
        dalle_amount
    ))[0]

    # TODO: Code starting to look a little spaghetti. Clean up once API works.

    artist_text = ''
    title_text = ''

    if provider_type == ProvidersConst.HISTORIC.value:
        # Historic image load
        # TODO: This needs to be refactored into external not historic
        image_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), image_location)

        if not os.path.exists(image_directory):
            warnings.warn("Image directory path does not exist: '" + image_directory + "'")
            exit()

        # Get random image from folder

        file = FileLoader(image_directory)
        image_path = file.get_random_file_of_type(image_format)

        image_base = Image.open(image_path)

        # Add text to via parsing if necessary
        image_name = os.path.basename(image_path)

        title_text = image_name

        if parse_text:
            title_text, artist_text = FileLoader.get_title_and_artist(image_name, preamble_regex, artist_regex,
                                                                      image_format)
            title_text = FileLoader.remove_text(title_text, remove_text)
            artist_text = FileLoader.remove_text(artist_text, remove_text)
            title_text = title_text.title()
            artist_text = artist_text.title()

        # Resize to thumbnail size based on epd resolution
        # TODO: allow users to choose between crop and resize
        epd_res = (epd.width, epd.height)
        image_base.thumbnail(epd_res)
    else:
        # Build prompt
        if prompt_mode == 0:
            # Pick random type of building
            random.seed()
            prompt_mode = random.randint(1, ConfigConst.PROMPT_MODES_COUNT.value)

        if prompt_mode == 1:
            # Build prompt from artist/subject
            artist_text = FileLoader.get_random_line(filepath + '/' + artists_file)
            title_text = FileLoader.get_random_line(filepath + '/' + subjects_file)
            prompt = preamble + title_text + ' ' + connector + ' ' + artist_text + postscript

        elif prompt_mode == 2:
            # Build prompt from artist/subject
            title_text = FileLoader.get_random_line(filepath + '/' + prompts_file)
            prompt = preamble + title_text + postscript

        else:
            warnings.warn('Invalid prompt mode chosen. Exiting application.')
            exit()

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
            stable_height = ceiling_multiple(epd.height, StabilityConst.MULTIPLE.value)
            stable_width = ceiling_multiple(epd.width, StabilityConst.MULTIPLE.value)
            image_base = stability_provider.get_image_from_string(prompt, stable_height, stable_width)
            if save_image:
                # TODO: Set up to save in internal location for Historic loading
                logging.info(f"Saving image as")
                # Save the image
                image_base.save('api_output.png')

        if provider_type == ProvidersConst.DALLE.value:
            # Request image for DALLE
            warnings.warn('DALLE not yet implemented. Exiting application.')
            exit()

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
    draw = ImageDraw.Draw(image_base, 'RGBA')

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
    if add_text:
        # TODO: bottom box doesn't look great if image crops with black space on the top and bottom
        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), font_file)
        if not os.path.exists(font_path):
            logging.info("Font file path does not exist: '" + font_file + "'")
            exit()

        title_font = ImageFont.truetype(font_path, title_size)
        artist_font = ImageFont.truetype(font_path, artist_size)

        if artist_text != '':
            artist_box = draw.textbbox((epd.width / 2, epd.height - artist_loc), artist_text, font=artist_font,
                                       anchor='mb')
        if title_text != '':
            title_box = draw.textbbox((epd.width / 2, epd.height - title_loc), title_text, font=title_font, anchor='mb')

        draw_box = max_area([artist_box, title_box])
        draw_box = tuple(numpy.add(draw_box, (-padding, -padding, padding, padding)))

        # Modify depending on box type
        if box_to_floor:
            draw_box = set_tuple_bottom(draw_box, bottom_pixel)

        if box_to_edge:
            draw_box = set_tuple_sides(draw_box, width_diff, right_pixel)

        draw.rectangle(draw_box, fill=(255, 255, 255, opacity))
        draw.text((epd.width / 2, epd.height - artist_loc), artist_text, font=artist_font, anchor='mb', fill=0)
        draw.text((epd.width / 2, epd.height - title_loc), title_text, font=title_font, anchor='mb', fill=0)

    logging.info("Prepare epaper")
    epd.prepare()

    epd.display(image_base)

    logging.info("Send epaper to sleep")
    epd.close()
    logging.shutdown()

except EPDNotFoundError:
    logging.info(f"Couldn't find {display_type}")
    exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.close()
    exit()
