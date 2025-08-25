import RPi.GPIO as GPIO
from time import sleep

# pinOut=5  # CH1
pinOut=6  # CH2
# pinOut=13 # CH3
# pinOut=16 # CH4
# pinOut=19 # CH5
# pinOut=20 # CH6
# pinOut=21 # CH7
# pinOut=26 # CH8

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinOut,GPIO.OUT)

def trigger(pinOut):
	print("starting low")
	GPIO.output(pinOut, GPIO.LOW)
	print ("waiting 2s")
	sleep(2)
	print("continuing high")
	GPIO.output(pinOut, GPIO.HIGH)
	#GPIO.cleanup()