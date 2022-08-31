#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
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


logging.basicConfig(level=logging.DEBUG)  # TODO: config out the logging level

# Set Defaults

# File Settings
image_location = ConfigConst.DEFAULT_IMAGE_LOCATION.value
image_format = ConfigConst.DEFAULT_IMAGE_FORMAT.value
font_file = ConfigConst.DEFAULT_FONT_FILE.value

# Text Settings
add_text = ConfigConst.DEFAULT_ADD_TEXT.value
parse_text = ConfigConst.DEFAULT_PARSE_TEXT.value
preamble_regex = ConfigConst.DEFAULT_PREAMBLE_REGEX.value
artist_regex = ConfigConst.DEFAULT_ARTIST_REGEX.value
remove_text = ConfigConst.DEFAULT_REMOVE_TEXT.value
box_to_floor = ConfigConst.DEFAULT_BOX_TO_FLOOR.value
box_to_edge = ConfigConst.DEFAULT_BOX_TO_EDGE.value
artist_loc = ConfigConst.DEFAULT_ARTIST_LOC.value
artist_size = ConfigConst.DEFAULT_ARTIST_SIZE.value
title_loc = ConfigConst.DEFAULT_TITLE_LOC.value
title_size = ConfigConst.DEFAULT_TITLE_SIZE.value
padding = ConfigConst.DEFAULT_PADDING.value
opacity = ConfigConst.DEFAULT_OPACITY.value

# Display Settings
display_type = ConfigConst.DEFAULT_DISPLAY_TYPE.value

# Provider Settings
historic_amount = ProvidersConst.HISTORIC_AMOUNT.value
stability_ai_amount = ProvidersConst.STABLE_AMOUNT.value
dalle_amount = ProvidersConst.DALLE_AMOUNT.value

# Debug Settings
image_viewer = ConfigConst.DEFAULT_IMAGE_VIEWER.value

# TODO: pull this out and put into config_wrapper.py
config = {}
try:
    # Load config
    config_load = Configs()
    if os.path.exists(ConfigConst.DEFAULT_CONFIG_PATH.value):
        config = config_load.read_config(ConfigConst.DEFAULT_CONFIG_PATH.value)
        logging.info('Loading config')

        # File Settings

        image_location = config.get('File', 'image_location', fallback=ConfigConst.DEFAULT_IMAGE_LOCATION.value)
        image_format = config.get('File', 'image_format', fallback=ConfigConst.DEFAULT_IMAGE_LOCATION.value)
        font_file = config.get('File', 'font_file', fallback=ConfigConst.DEFAULT_FONT_FILE.value)

        # Text Settings
        add_text = config.getboolean('Text', 'add_text', fallback=ConfigConst.DEFAULT_ADD_TEXT.value)
        parse_text = config.getboolean('Text', 'parse_text', fallback=ConfigConst.DEFAULT_PARSE_TEXT.value)
        preamble_regex = config.get('Text', 'preamble_regex', fallback=ConfigConst.DEFAULT_PREAMBLE_REGEX.value)
        artist_regex = config.get('Text', 'artist_regex', fallback=ConfigConst.DEFAULT_ARTIST_REGEX.value)
        remove_text = config.get('Text', 'remove_text', fallback=ConfigConst.DEFAULT_REMOVE_TEXT.value).split('\n')
        box_to_floor = config.getboolean('Text', 'box_to_floor', fallback=ConfigConst.DEFAULT_BOX_TO_FLOOR.value)
        box_to_edge = config.getboolean('Text', 'box_to_edge', fallback=ConfigConst.DEFAULT_BOX_TO_EDGE.value)
        artist_loc = config.getint('Text', 'artist_loc', fallback=ConfigConst.DEFAULT_ARTIST_LOC.value)
        artist_size = config.getint('Text', 'artist_size', fallback=ConfigConst.DEFAULT_ARTIST_SIZE.value)
        title_loc = config.getint('Text', 'title_loc', fallback=ConfigConst.DEFAULT_TITLE_LOC.value)
        title_size = config.getint('Text', 'title_size', fallback=ConfigConst.DEFAULT_TITLE_SIZE.value)
        padding = config.getint('Text', 'padding', fallback=ConfigConst.DEFAULT_PADDING.value)
        opacity = config.getint('Text', 'opacity', fallback=ConfigConst.DEFAULT_OPACITY.value)

        # Display (rest of EPD config is just passed straight into displayfactory
        display_type = config.get('EPD', 'type', fallback=ConfigConst.DEFAULT_DISPLAY_TYPE.value)

        # Provider
        historic_amount = config.get('Providers', 'historic_amount', fallback=ProvidersConst.HISTORIC_AMOUNT.value)
        stability_ai_amount = config.get('Providers', 'historic_amount', fallback=ProvidersConst.STABLE_AMOUNT.value)
        dalle_amount = config.get('Providers', 'historic_amount', fallback=ProvidersConst.DALLE_AMOUNT.value)

        # Debug Settings
        image_viewer = config.getboolean('DEBUG', 'image_viewer', fallback=ConfigConst.DEFAULT_IMAGE_VIEWER.value)

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
    # request key if it doesn't already exist. TODO: put this into a new configure.py

    image_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), image_location)
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), font_file)
    if not os.path.exists(image_directory):
        logging.info("Image directory path does not exist: '" + image_directory + "'")
        exit()

    if not os.path.exists(font_path):
        logging.info("font file path does not exist: '" + font_file + "'")
        exit()

    # Get random image from folder

    file = FileLoader(image_directory)
    image_path = file.get_random_file_of_type(image_format)
    logging.info(image_path)

    title_font = ImageFont.truetype(font_path, title_size)
    artist_font = ImageFont.truetype(font_path, artist_size)

    logging.info("Displaying Test Image")
    image_base = Image.open(image_path)
    logging.info(image_base.width)

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

    # Add text to image
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

    if add_text:
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
