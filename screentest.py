#!/usr/bin/python
# -*- coding:utf-8 -*-

# Screen test based on epd_7in5_V2_test.py

import sys
import os

contentDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testcontent')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("pycasso test image display")
    epd = epd7in5_V2.EPD()

    logging.info("init and clear")
    epd.init()
    epd.Clear()

    # temp logging to understand how content directory is being handled
    logging.info(os.path.join(contentDirectory))

    font24 = ImageFont.truetype(os.path.join(contentDirectory, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(contentDirectory, 'Font.ttc'), 18)

    logging.info("Displaying Test Image")
    logging.info(os.path.join(contentDirectory))
    imageBase = Image.open(os.path.join(contentDirectory, 'test.png'))
    logging.info(imageBase.width)

    # TODO: fix hard coded tuple to dynamic
    imageBase = imageBase.crop((0, 0, 800, 480))
    logging.info(imageBase.width)
    logging.info(imageBase.height)
    draw = ImageDraw.Draw(imageBase)

    # TODO: do we need the rectangle? place it elsewhere maybe
    draw.rectangle((80, 50, 130, 100), fill=0)

    # TODO: place text dynamically
    draw.text((2, 0), 'Cool Bird Wearing Glasses', font=font24, fill=0)
    draw.text((2, 0), 'Lichtenstein', font=font24, fill=0)
    epd.display(epd.getbuffer(imageBase))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
