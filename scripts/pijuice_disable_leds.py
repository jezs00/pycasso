#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Python script to disable LEDs on pijuice to avoid draining battery unnecessarily

from pijuice import PiJuice
from piblo.pijuice_handler import PiJuiceHandler
import logging

pijuice = PiJuice(1, 0x14)
PiJuiceHandler.pijuice_led_disable(pijuice)
logging.info("LEDs disabled on pijuice unit")
print("LEDs disabled on pijuice unit")
