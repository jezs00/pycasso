#!/usr/bin/python
# -*- coding:utf-8 -*-

# Screen test based on epd_7in5_V2_test.py

import sys
import os

contentDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testcontent')
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
#if os.path.exists(libdir):
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

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(contentDirectory, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(contentDirectory, 'Font.ttc'), 18)

    logging.info("Displaying Test Image")
    imageBase = Image.open(os.path.join(contentDirectory, "DALL·E 2022-07-11 07.31.17 - cool bird wearing glasses in the style of lichtenstein, digital art.png"))
    draw = ImageDraw.Draw(imageBase)
    draw.rectangle((80, 50, 130, 100), fill=0)
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