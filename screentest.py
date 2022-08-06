#!/usr/bin/python
# -*- coding:utf-8 -*-

# Simple screen test based on epd_7in5_V2_test.py

import os

contentDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testcontent')

import logging
# TODO: refactor with omni-epd https://github.com/robweber/omni-epd
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageShow
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("pycasso test image display")
    epd = epd7in5_V2.EPD()

    logging.info("Init and clear screen")
    epd.init()
    epd.Clear()

    fileLocation = os.path.join(contentDirectory, 'test.png')

    logging.info("Loading " + fileLocation)
    imageBase = Image.open(fileLocation)

    logging.info("Resizing image")
    # Resize to thumbnail size based on epd resolution
    epdResolution = (epd.width, epd.height)
    logging.info(epdResolution)
    imageBase.thumbnail(epdResolution)

    # Make sure image is correct size and centered after thumbnail set
    # Define locations and crop settings
    widthDiff = (epd.width - imageBase.width) / 2
    heightDiff = (epd.height - imageBase.height) / 2
    leftPixel = 0 - widthDiff
    topPixel = 0 - heightDiff
    rightPixel = imageBase.width + widthDiff
    bottomPixel = imageBase.height + heightDiff
    imageCrop = (leftPixel, topPixel, rightPixel, bottomPixel)

    # Crop and prepare image
    imageBase = imageBase.crop(imageCrop)

    logging.info("Displaying image")
    epd.display(epd.getbuffer(imageBase))

    # Show image if OS has an image viewer
    ImageShow.show(imageBase)
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
