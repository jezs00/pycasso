#!/usr/bin/python
# -*- coding:utf-8 -*-

# Simple screen test based on epd_7in5_V2_test.py

import os
import logging
import time
# TODO: refactor with omni-epd https://github.com/robweber/omni-epd
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageShow

logging.basicConfig(level=logging.DEBUG)

try:
    content_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testcontent')

    logging.info("pycasso test image display")
    epd = epd7in5_V2.EPD()

    logging.info("Init and clear screen")
    epd.init()
    epd.Clear()

    fileLocation = os.path.join(content_directory, 'test.png')

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
    epd.display(epd.getbuffer(image_base))

    # Show image if OS has an image viewer
    ImageShow.show(image_base)
    time.sleep(2)

    logging.info("Go to sleep...")
    epd.sleep()

    logging.info("Check the screen to see if it worked")

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
