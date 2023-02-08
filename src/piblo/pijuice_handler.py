#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Handler file to run pycasso when using pijuice

import logging
import os
import sys
import time

from pijuice import PiJuice

from piblo.pycasso import Pycasso
from piblo.constants import PiJuiceConst, DisplayShapeConst


class PiJuiceHandler:

    def __init__(self):

        return

    @staticmethod
    def safe_pijuice_shutdown(pijuice):
        # Remove power to PiJuice MCU IO pins
        pijuice.power.SetSystemPowerSwitch(0)

        # In 5 seconds we are not so nice - Remove 5V power to RPi
        pijuice.power.SetPowerOff(5)

        # Enable wakeup alarm
        pijuice.rtcAlarm.SetWakeupEnabled(True)

        # But try to shut down nicely first
        os.system("sudo shutdown -h 0")
        sys.exit()

    @staticmethod
    def system_shutdown():
        os.system("shutdown /s /t 1")
        sys.exit()

    @staticmethod
    def pijuice_led_disable(pijuice):
        led_config = {'function': 'NOT_USED', 'parameter': {'r': 0, 'g': 0, 'b': 0}}
        pijuice.config.SetLedConfiguration('D1', led_config)
        pijuice.config.SetLedConfiguration('D2', led_config)
        return

    def run(self):
        try:
            instance = Pycasso()
        except Exception as e:
            logging.error(e)
            logging.error("Cannot create Pycasso object. Exiting process.")
            sys.exit()

        # Set config variables based on config that pycasso loaded
        sleep_time = instance.config.wait_to_run
        shutdown = instance.config.shutdown_on_battery
        shutdown_ex = instance.config.shutdown_on_exception

        power_status = None
        charge_level = -1

        # sleep for a bit as I can't figure out a better solution to stop pijuice from failing to start
        time.sleep(sleep_time)
        try:
            pijuice = PiJuice(1, 0x14)
            power_status = pijuice.status.GetStatus()[PiJuiceConst.STATUS_ROOT.value][PiJuiceConst.STATUS_POWER.value]
            charge_level = pijuice.status.GetChargeLevel()['data']
            instance.charge_level = charge_level

        except Exception as e:
            logging.error(e)
            logging.error("Cannot create pijuice object. Running pycasso once with error display and exiting process.")
            # run pycasso with error symbol, then exit
            instance.add_exception_icon()
            instance.run()

            if shutdown_ex:
                logging.info(f"Shutting down if possible. Waiting {sleep_time} seconds before sending signal")
                time.sleep(sleep_time)
                self.system_shutdown()
                sys.exit()

        logging.info(f"Power status is \'{power_status}\'")
        logging.info(f"Battery level is \'{charge_level}\'")

        try:
            instance.run()

            if power_status == PiJuiceConst.NOT_PRESENT.value:
                # shutdown if we've configured pycasso to do so
                if shutdown:
                    self.safe_pijuice_shutdown(pijuice)

        except Exception as e:
            logging.error(e)

            # shutdown if we've configured pycasso to do so
            if shutdown_ex:
                logging.info(f"Shutting down if possible. Waiting {sleep_time} seconds before sending signal")
                time.sleep(sleep_time)
                self.safe_pijuice_shutdown(pijuice)
            sys.exit()

        return
