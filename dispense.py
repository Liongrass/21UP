# Modules
import logging
from gpiozero import OutputDevice
from time import sleep

# Functions and variables
from var import pin_out, relay_duration

device = [OutputDevice(pin, initial_value=False) for pin in pin_out]

def trigger(pinOut, tray):
	logging.debug(device[tray])
	device[tray].on()
	logging.info(f"Dispensing tray {tray} at pin {pin_out[tray]}")
	logging.debug(f"waiting {relay_duration}s")
	sleep(relay_duration)
	device[tray].off()
	logging.info(f"Done dispensing tray {tray}")