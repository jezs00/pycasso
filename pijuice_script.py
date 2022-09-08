#!/usr/bin/python3

from pijuice import PiJuice
import logging
import os
import sys

try:
	pijuice = PiJuice(1, 0x14)
except:
	print("Cannot create pijuice object")
	sys.exit()

# TODO: set constants for pijuice statuses

power_status = pijuice.status.GetStatus()['data']['powerInput']

logging.info(f"Power status is \'{power_status}\'")

if power_status == 'NOT_PRESENT':
	# If power not plugged in, run pycasso and shut down
	os.system(f"sudo dbus-run-session -- bash {os.path.dirname(os.path.abspath(__file__))}/run.sh")
	
	# Remove power to PiJuice MCU IO pins
	pijuice.power.SetSystemPowerSwitch(0)

	# In 10 seconds we are not so nice - Remove 5V power to RPi
	pijuice.power.SetPowerOff(10)

	# But try to shut down nicely first
	os.system("sudo shutdown -h 0")

