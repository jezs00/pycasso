#!/usr/bin/python3

from pijuice import PiJuice
import logging
import os
import sys
from constants import PiJuiceConst

# Set up logging
file_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO, filename=os.path.join(file_path, 'pijuice.log'))

try:
	pijuice = PiJuice(1, 0x14)
except:
	logging.error("Cannot create pijuice object")
	sys.exit()

# TODO: handle error pijuice not available

power_status = pijuice.status.GetStatus()[PiJuiceConst.STATUS_ROOT.value][PiJuiceConst.STATUS_POWER.value]

logging.info(f"Power status is \'{power_status}\'")

if power_status == PiJuiceConst.NOT_PRESENT.value:
	# If power not plugged in, run pycasso and shut down
	os.system(f"sudo dbus-run-session -- bash {os.path.dirname(os.path.abspath(__file__))}/run.sh")

	# Remove power to PiJuice MCU IO pins
	pijuice.power.SetSystemPowerSwitch(0)

	# In 10 seconds we are not so nice - Remove 5V power to RPi
	pijuice.power.SetPowerOff(10)

	# Enable wakeup alarm
	pijuice.rtcAlarm.SetWakeupEnabled(True)

	# But try to shut down nicely first
	os.system("sudo shutdown -h 0")
