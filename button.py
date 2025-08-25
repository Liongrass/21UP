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
def listener():
    print("Button was pressed!")
    asyncio.run(payment())

try:
    while True:
        is_pressed = GPIO.input(pinIn)

        # Check if the button is currently pressed AND it wasn't pressed before
        if is_pressed and not was_pressed:
            listener()
        
        # Update the state for the next loop
        was_pressed = is_pressed
        
        # A small delay to prevent excessive CPU usage
        sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()