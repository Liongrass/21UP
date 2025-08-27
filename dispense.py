# Modules
import RPi.GPIO as GPIO
from time import sleep

# Functions and variables
from var import pin_out, relay_duration

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_out,GPIO.OUT)

def trigger(pinOut, tray):
	print(f"Dispensing tray {tray} at pin {pin_out[tray]}")
	GPIO.output(pin_out[tray], GPIO.LOW)
	print ("waiting 2s")
	sleep(relay_duration)
	print(f"Done dispensing tray {tray}")
	GPIO.output(pin_out[tray], GPIO.HIGH)
	#GPIO.cleanup()