# Modules
import RPi.GPIO as GPIO
from time import sleep
import asyncio

# Functions and variables
from payments import payment
from var import pin_in, button_delay

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

async def listener():
    while True:
        detected = False
        for i in pin_in:
            if GPIO.input(i):
                detected = True
                global tray
                tray = pin_in.index(i)
                item = i
                sleep(button_delay)
        if detected:
            print(f"Pin {item} pressed. Fetching payment for tray {tray}")
            await payment(tray)
        # if an event remains high for more than 0.5 sec it might
        # be counted again on the next loop. Likewise if an event
        # comes and goes before the next loop it will be missed.
        #sleep(0.5)