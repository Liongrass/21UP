# Modules
from gpiozero import OutputDevice
from time import sleep

# Functions and variables
from var import pin_out, relay_duration

device = [OutputDevice(pin, initial_value=True) for pin in pin_out]

def trigger(pinOut, tray):
	print("YOYO")
	print(device[tray])
	print(f"Dispensing tray {tray} at pin {pin_out[tray]}")
	device[tray].off()
	print (f"waiting {relay_duration}s")
	sleep(relay_duration)
	print(f"Done dispensing tray {tray}")
	device[tray].on()