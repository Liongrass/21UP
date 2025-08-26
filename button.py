# Modules
import RPi.GPIO as GPIO
from time import sleep
import asyncio

# Functions and variables
from payments import payment

pinIn=17

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Assume the button is not currently pressed
was_pressed = True

# Function that waits for the button to be pressed
async def listener():
    while True:
        is_pressed = GPIO.input(pinIn)
        if is_pressed and not was_pressed:
            print("Button was pressed!")
            sleep(0.5)
            await payment()
            sleep(0.5)
        was_pressed = is_pressed