# Modules
import asyncio
from gpiozero import Button
import logging
from time import sleep

# Functions and variables
from payments import payment
from qr import make_description
from var import pin_in, button_delay

# Set up GPIO
buttons = [Button(btn, pull_up=False) for btn in pin_in]

async def listener():
    logging.info(f"listening on pins {pin_in}")
    while True:
        detected = False
        for btn in buttons:
            if not btn.is_held and btn.is_pressed:
                detected = True
                global tray
                tray = buttons.index(btn)
                item = btn
                await asyncio.sleep(button_delay)
        if detected:
            logging.info(f"Pin {pin_in[tray]} pressed. Fetching payment for tray {tray}")
            logging.debug(item)
            make_description(tray)
            await payment(tray)
            logging.info(f"listening on pins {pin_in}")
        # if an event remains high for more than 0.5 sec it might
        # be counted again on the next loop. Likewise if an event
        # comes and goes before the next loop it will be missed.
        sleep(button_delay)