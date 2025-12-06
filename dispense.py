# Modules
import logging
from gpiozero import OutputDevice
from time import sleep

# Functions and variables
from var import pin_hot, pin_out, relay_duration

device = [OutputDevice(pin, initial_value=False) for pin in pin_out]
hotpin = OutputDevice(pin_hot, initial_value=False)

def trigger(pinOut, tray):
	hotpin.on()
	logging.debug(f"Making machine hot at pin {pin_hot}")
	logging.debug(device[tray])
	device[tray].on()
	logging.info(f"Dispensing tray {tray} at pin {pin_out[tray]}")
	logging.debug(f"waiting {relay_duration}s")
	sleep(relay_duration)
	device[tray].off()
	logging.info(f"Done dispensing tray {tray}")
	hotpin.off()
	logging.debug(f"Making machine cold at pin {pin_hot}")