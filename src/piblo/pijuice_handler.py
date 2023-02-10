#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Handler file to run pycasso when using pijuice

import logging
import os
import sys
import time

from pijuice import PiJuice

from piblo.pycasso import Pycasso
from piblo.constants import PiJuiceConst, BatteryConst


class PiJuiceHandler:
    """
    A class used to provide image operations for pycasso.

    Attributes
    ----------

    Methods
    -------
    safe_pijuice_shutdown(pijuice)
        Uses PiJuice to attempt to shut down safely and completely using pijuice object 'pijuice'.

    system_shutdown()
        Uses linux system command to shut down.

    pijuice_led_disable(pijuice)
        Uses PiJuice to disable LEDs on board with pijuice object 'pijuice'.

    get_charge_status(power_status, charge_level)
        Returns valid charge level or constant to be passed to pycasso for battery display. Uses valid pijuice
        power_status and charge_level

    def run(self):
        Attempts to run pycasso based on configuration and pijuice settings.
    """
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

    @staticmethod
    def get_charge_status(power_status, charge_level):
        if power_status == PiJuiceConst.NOT_PRESENT.value:
            charge_level = charge_level
        elif power_status == PiJuiceConst.PRESENT.value:
            charge_level = BatteryConst.CHARGING.value
        elif power_status == PiJuiceConst.WEAK.value:
            charge_level = BatteryConst.WEAK.value
        elif power_status == PiJuiceConst.BAD.value:
            charge_level = BatteryConst.BAD.value
        else:
            charge_level = BatteryConst.ERROR.value

        return charge_level

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
        charge_level = BatteryConst.ERROR.value

        # sleep for a bit as I can't figure out a better solution to stop pijuice from failing to start
        time.sleep(sleep_time)
        try:
            pijuice = PiJuice(1, 0x14)
            power_status = pijuice.status.GetStatus()[PiJuiceConst.STATUS_ROOT.value][PiJuiceConst.STATUS_POWER.value]
            charge_level = pijuice.status.GetChargeLevel()['data']
            instance.charge_level = PiJuiceHandler.get_charge_status(power_status, charge_level)

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
