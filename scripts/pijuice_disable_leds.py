#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Python script to disable LEDs on pijuice to avoid draining battery unnecessarily

from piblo.pijuice_handler import PiJuiceHandler

PiJuiceHandler.pijuice_led_disable()
