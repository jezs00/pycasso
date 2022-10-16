#!/usr/bin/python3

from pijuice import PiJuice

from pycasso import Pycasso
import logging
import os
import sys
from constants import PiJuiceConst, DisplayShape

# Set up logging
file_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO, filename=os.path.join(file_path, "pijuice.log"))

power_status = PiJuiceConst.NOT_PRESENT.value
charge_level = 100

try:
	pijuice = PiJuice(1, 0x14)
	power_status = pijuice.status.GetStatus()[PiJuiceConst.STATUS_ROOT.value][PiJuiceConst.STATUS_POWER.value]
	charge_level = pijuice.status.GetChargeLevel()['data']
except:
	logging.error("Cannot create pijuice object. Running pycasso once with error display and exiting process.")
	# run pycasso with error symbol, then exit
	instance = Pycasso()
	instance.icon_shape = DisplayShape.CROSS
	instance.run()
	sys.exit()

logging.info(f"Power status is \'{power_status}\'")
logging.info(f"Battery level is \'{charge_level}\'")

if power_status == PiJuiceConst.NOT_PRESENT.value:
	# If power not plugged in, run pycasso and shut down
	instance = Pycasso()

	# Set icon if PiJuice has lower battery
	if charge_level < PiJuiceConst.CHARGE_DISPLAY.value:
		logging.info(f"Displaying icon due to low battery")
		instance.icon_shape = DisplayShape.SQUARE
	
	instance.run()
	
	# Remove power to PiJuice MCU IO pins
	pijuice.power.SetSystemPowerSwitch(0)

	# In 10 seconds we are not so nice - Remove 5V power to RPi
	pijuice.power.SetPowerOff(10)

	# Enable wakeup alarm
	pijuice.rtcAlarm.SetWakeupEnabled(True)

	# But try to shut down nicely first
	os.system("sudo shutdown -h 0")
