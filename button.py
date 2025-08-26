# Modules
import RPi.GPIO as GPIO
from time import sleep
import asyncio

# Functions and variables
from payments import payment, stop_process

pinInA=17
pinInB=27
pinInC=22

pin_list = [17, 27, 22]
counts = { ch: 0 for ch in pin_list }

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

async def listener():
    while True:
        detected = False
        for ch in pin_list:
            if GPIO.input(ch):
                detected = True
                counts[ch] += 1
        if detected:
            print(counts)
            for ch in pin_list:
                counts[ch] = 0
        # if an event remains high for more than 0.5 sec it might
        # be counted again on the next loop. Likewise if an event
        # comes and goes before the next loop it will be missed.
        sleep(0.5)