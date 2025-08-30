# Modules
from gpiozero import Button
from time import sleep
import asyncio

# Functions and variables
from payments import payment
from var import pin_in, button_delay

# Set up GPIO
buttons = [Button(btn, pull_up=False) for btn in pin_in]

async def listener():
    print(f"listening on pins {pin_in}")
    while True:
        detected = False
        for btn in buttons:
            if btn.is_pressed:
                detected = True
                global tray
                tray = buttons.index(btn)
                item = btn
                sleep(button_delay)
        if detected:
            print(f"Pin {item} pressed. Fetching payment for tray {tray}")
            await payment(tray)
        # if an event remains high for more than 0.5 sec it might
        # be counted again on the next loop. Likewise if an event
        # comes and goes before the next loop it will be missed.
        #sleep(0.5)