#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import random
import warnings

import numpy

import logging
from config_wrapper import Configs
from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image, ImageDraw, ImageFont
from file_loader import FileLoader
from constants import ProvidersConst, StabilityConst, ConfigConst

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

logging.basicConfig(level=logging.DEBUG)  # TODO: config out the logging level

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

# Debug Settings
image_viewer = ConfigConst.DEBUG_IMAGE_VIEWER.value

# TODO: pull this out and put into config_wrapper.py
config = {}
try:
    # Load config
    config_load = Configs()
    if os.path.exists(ConfigConst.CONFIG_PATH.value):
        config = config_load.read_config(ConfigConst.CONFIG_PATH.value)
        logging.info('Loading config')

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

        # Debug Settings
        image_viewer = config.getboolean('Debug', 'image_viewer', fallback=ConfigConst.DEBUG_IMAGE_VIEWER.value)

except IOError as e:
    logging.error(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

logging.info("pycasso has begun")

try:
    epd = displayfactory.load_display_driver(display_type, config)

except EPDNotFoundError:
    logging.info(f"Couldn't find {display_type}")
    exit()

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

try:
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

    logging.info(provider_type)

    # TODO: Code starting to look a little spaghetti. Clean up once API works.

    if provider_type == ProvidersConst.HISTORIC.value:
        image_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), image_location)

        if not os.path.exists(image_directory):
            logging.info("Image directory path does not exist: '" + image_directory + "'")
            exit()

        # Get random image from folder

        file = FileLoader(image_directory)
        image_path = file.get_random_file_of_type(image_format)
        logging.info(image_path)

        image_base = Image.open(image_path)
        logging.info(image_base.width)

        # Add text to via parsing if necessary
        image_name = os.path.basename(image_path)

        artist_text = ''
        title_text = image_name

        if parse_text:
            title_text, artist_text = FileLoader.get_title_and_artist(image_name, preamble_regex, artist_regex,
                                                                      image_format)
            title_text = FileLoader.remove_text(title_text, remove_text)
            artist_text = FileLoader.remove_text(artist_text, remove_text)
            title_text = title_text.title()
            artist_text = artist_text.title()
    else:
        # Build prompt
        if prompt_mode == 0:
            # Pick random type of building
            random.seed()
            prompt_mode = random.randint(1, ConfigConst.PROMPT_MODES_COUNT.value)

        if prompt_mode == 1:
            # Build prompt from artist/subject
            artist_text = FileLoader.get_random_line(artists_file)
            title_text = FileLoader.get_random_line(subjects_file)
            prompt = preamble + title_text + ' ' + connector + ' ' + artist_text + postscript

        elif prompt_mode == 2:
            # Build prompt from artist/subject
            title_text = FileLoader.get_random_line(prompts_file)
            prompt = preamble + title_text + postscript

        else:
            warnings.warn('Invalid prompt mode chosen. Exiting application.')
            exit()

        # Pick between providers
        if provider_type == ProvidersConst.STABLE.value:
            # Request image for Stability
            warnings.warn('Stability not yet implemented. Exiting application.')
            exit()

        if provider_type == ProvidersConst.DALLE.value:
            # Request image for DALLE
            warnings.warn('DALLE not yet implemented. Exiting application.')
            exit()

    # Resize to thumbnail size based on epd resolution
    epd_res = (epd.width, epd.height)
    image_base.thumbnail(epd_res)

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
    logging.info(image_base.width)
    logging.info(image_base.height)
    draw = ImageDraw.Draw(image_base, 'RGBA')

    if add_text:
        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), font_file)
        if not os.path.exists(font_path):
            logging.info("Font file path does not exist: '" + font_file + "'")
            exit()

        title_font = ImageFont.truetype(font_path, title_size)
        artist_font = ImageFont.truetype(font_path, artist_size)

        artist_box = draw.textbbox((epd.width / 2, epd.height - artist_loc), artist_text, font=artist_font, anchor='mb')
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

    logging.info("Prepare")
    epd.prepare()

    epd.display(image_base)

    logging.info("Go to sleep...")
    epd.close()

except EPDNotFoundError:
    logging.info(f"Couldn't find {display_type}")
    exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.close()
    exit()
