#!/usr/bin/python
# -*- coding:utf-8 -*-

# Simple screen test based on epd_7in5_V2_test.py

import os
import logging
import time
import config_wrapper
from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image, ImageShow

# Relative path to config
CONFIG_PATH = ".config"

# Display Settings
DEFAULT_DISPLAY_TYPE = "omni_epd.mock"

logging.basicConfig(level=logging.DEBUG)

display_type = DEFAULT_DISPLAY_TYPE

try:
    # Load config
    if os.path.exists(CONFIG_PATH):
        config_load = config_wrapper.Configs(CONFIG_PATH)
        config = config_load.read_config()
        logging.info("Loading config")

        # Display Settings
        display_type = config.get("EPD", "type")

except IOError as e:
    logging.error(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    exit()

try:
    epd = displayfactory.load_display_driver(display_type)

    content_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tests/test_file_operations_content")

    logging.info("pycasso test image display")

    logging.info("Init and clear screen")
    epd.prepare()

    fileLocation = os.path.join(content_directory, "test.png")

    logging.info("Loading " + fileLocation)
    image_base = Image.open(fileLocation)

    logging.info("Resizing image")
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

    logging.info("Displaying image")
    epd.display(image_base)

    # Show image if OS has an image viewer
    time.sleep(2)

    logging.info("Go to sleep...")
    epd.close()

    logging.info("Check the screen to see if it worked")

except EPDNotFoundError:
    logging.info(f"Couldn't find {display_type}")
    exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.close()
    exit()
