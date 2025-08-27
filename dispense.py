import RPi.GPIO as GPIO
from time import sleep

pin_out = [5, 6, 13]

# pinOut=5  # CH1
# pinOut=6  # CH2
# pinOut=13 # CH3
# pinOut=16 # CH4
# pinOut=19 # CH5
# pinOut=20 # CH6
# pinOut=21 # CH7
# pinOut=26 # CH8

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_out,GPIO.OUT)

def trigger(pinOut, tray):
	print(f"Dispensing tray {tray} at pin {pin_out[tray]}")
	GPIO.output(pin_out[tray], GPIO.LOW)
	print ("waiting 2s")
	sleep(2)
	print(f"Done dispensing tray {tray}")
	GPIO.output(pin_out[tray], GPIO.HIGH)
	#GPIO.cleanup()