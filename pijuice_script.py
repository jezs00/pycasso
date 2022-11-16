#!/usr/bin/python3

from pijuice import PiJuice
from pycasso import Pycasso
import logging
import os
import sys
import time
from constants import PiJuiceConst, DisplayShape

# Set up logging
file_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO, filename=os.path.join(file_path, "pycasso.log"))

power_status = None
charge_level = 100

# sleep for a bit as I can't figure out a better solution to stop pijuice from failing to start
time.sleep(30) #TODO set up constant and config for wait time

try:
	pijuice = PiJuice(1, 0x14)
	power_status = pijuice.status.GetStatus()[PiJuiceConst.STATUS_ROOT.value][PiJuiceConst.STATUS_POWER.value]
	charge_level = pijuice.status.GetChargeLevel()['data']
except:
	logging.error("Cannot create pijuice object. Running pycasso once with error display and exiting process.")
	# run pycasso with error symbol, then exit
	instance = Pycasso()
	instance.icon_shape = DisplayShape.CROSS.value
	instance.run()
	os.system("shutdown /s /t 1")
	sys.exit()

logging.info(f"Power status is \'{power_status}\'")
logging.info(f"Battery level is \'{charge_level}\'")
try:
	if power_status == PiJuiceConst.NOT_PRESENT.value:
		# If power not plugged in, run pycasso and shut down
		instance = Pycasso()

		# Set icon if PiJuice has lower battery
		if charge_level < PiJuiceConst.CHARGE_DISPLAY.value:
			logging.info(f"Displaying icon due to low battery")
			instance.icon_shape = DisplayShape.SQUARE.value

		instance.run()

		# Remove power to PiJuice MCU IO pins
		pijuice.power.SetSystemPowerSwitch(0)

		# In 10 seconds we are not so nice - Remove 5V power to RPi
		pijuice.power.SetPowerOff(10)

		# Enable wakeup alarm
		pijuice.rtcAlarm.SetWakeupEnabled(True)

		# But try to shut down nicely first
		os.system("sudo shutdown -h 0")

except:
	logging.error("Program Error. Shutting down if possible")
	# Remove power to PiJuice MCU IO pins
	pijuice.power.SetSystemPowerSwitch(0)

	# In 5 seconds we are not so nice - Remove 5V power to RPi
	pijuice.power.SetPowerOff(5)

	# Enable wakeup alarm
	pijuice.rtcAlarm.SetWakeupEnabled(True)

	# But try to shut down nicely first
	os.system("sudo shutdown -h 0")
