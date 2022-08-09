#!/usr/bin/python
# -*- coding:utf-8 -*-

# Screen test based on epd_7in5_V2_test.py

import sys
import os
import numpy
import config_wrapper
import logging
# TODO: refactor with omni-epd https://github.com/robweber/omni-epd
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont, ImageShow
from file_loader import FileLoader
import traceback

lib_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)

# Relative path to config
CONFIG_PATH = '.config'

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
DEFAULT_REMOVE_TEXT = ""
DEFAULT_BOX_TO_FLOOR = True
DEFAULT_BOX_TO_EDGE = True
DEFAULT_ARTIST_LOC = 10
DEFAULT_TITLE_LOC = 30
DEFAULT_PADDING = 10
DEFAULT_OPACITY = 150

# Debug Settings
DEFAULT_IMAGE_VIEWER = False


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


logging.basicConfig(level=logging.DEBUG)

# Set Defaults

# File Settings
image_location = DEFAULT_IMAGE_LOCATION
image_format = DEFAULT_IMAGE_FORMAT
font_file = DEFAULT_FONT_FILE

# Text Settings
add_text = DEFAULT_ADD_TEXT
parse_text = DEFAULT_PARSE_TEXT
preamble_regex = DEFAULT_PREAMBLE_REGEX
artist_regex = DEFAULT_ARTIST_REGEX
remove_text = DEFAULT_REMOVE_TEXT
box_to_floor = DEFAULT_BOX_TO_FLOOR
box_to_edge = DEFAULT_BOX_TO_EDGE
artist_loc = DEFAULT_ARTIST_LOC
title_loc = DEFAULT_TITLE_LOC
padding = DEFAULT_PADDING
opacity = DEFAULT_OPACITY

# Debug Settings
image_viewer = DEFAULT_IMAGE_VIEWER

try:
    # Load config
    if os.path.exists(CONFIG_PATH):
        config = config_wrapper.read_config(CONFIG_PATH)
        logging.info('Loading config')

        # File Settings
        image_location = config.get('FILE', 'image_location')
        image_format = config.get('FILE', 'image_format')
        font_file = config.get('FILE', 'font_file')

        # Text Settings
        add_text = config.getboolean('TEXT', 'add_text')
        parse_text = config.getboolean('TEXT', 'parse_text')
        preamble_regex = config.get('TEXT', 'preamble_regex')
        artist_regex = config.get('TEXT', 'artist_regex')
        # TODO: handle remove_text into tuple
        remove_text = ", digital art;A painting of ;an oil painting of ;a surrealist oil painting of ;graffiti of"
        box_to_floor = config.getboolean('TEXT', 'box_to_floor')
        box_to_edge = config.getboolean('TEXT', 'box_to_edge')
        artist_loc = config.getint('TEXT', 'artist_loc')
        title_loc = config.getint('TEXT', 'title_loc')
        padding = config.getint('TEXT', 'padding')
        opacity = config.getint('TEXT', 'opacity')

        # Debug Settings
        image_viewer = config.getboolean('DEBUG', 'image_viewer')

except IOError as e:
    logging.error(e)
    logging.info('Setting defaults:')
    # TODO: set up defaults on IO exception

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

try:
    # TODO: Put file not found handling here
    image_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), image_location)
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), font_file)
    logging.info(image_directory)
    logging.info(font_path)

    logging.info("pycasso")
    epd = epd7in5_V2.EPD()

    # Get random image from folder

    file = FileLoader(image_directory)
    image_path = file.get_random_file_of_type(image_format)
    logging.info(image_path)

    font24 = ImageFont.truetype(font_path, 24)
    font18 = ImageFont.truetype(font_path, 18)

    logging.info("Displaying Test Image")
    image_base = Image.open(image_path)
    logging.info(image_base.width)

    # Resize to thumbnail size based on epd resolution
    epd_res = (epd.width, epd.height)
    logging.info(epd_res)
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
        remove_text = (", digital art", "A painting of ", "an oil painting of ", "a surrealist oil painting of ",
                       "graffiti of ")
        title_text = FileLoader.remove_text(title_text, remove_text)
        artist_text = FileLoader.remove_text(artist_text, remove_text)
        title_text = title_text.title()
        artist_text = artist_text.title()

    if add_text:
        artist_box = draw.textbbox((epd.width / 2, epd.height - artist_loc), artist_text, font=font18, anchor='mb')
        title_box = draw.textbbox((epd.width / 2, epd.height - title_loc), title_text, font=font24, anchor='mb')

        draw_box = max_area([artist_box, title_box])
        draw_box = tuple(numpy.add(draw_box, (-padding, -padding, padding, padding)))

        # Modify depending on box type
        if box_to_floor:
            draw_box = set_tuple_bottom(draw_box, bottom_pixel)

        if box_to_edge:
            draw_box = set_tuple_sides(draw_box, width_diff, right_pixel)

        draw.rectangle(draw_box, fill=(255, 255, 255, opacity))
        draw.text((epd.width / 2, epd.height - artist_loc), artist_text, font=font18, anchor='mb', fill=0)
        draw.text((epd.width / 2, epd.height - title_loc), title_text, font=font24, anchor='mb', fill=0)

    logging.info("init and clear")
    epd.init()
    epd.Clear()

    epd.display(epd.getbuffer(image_base))

    if image_viewer:
        ImageShow.show(image_base)
        time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
