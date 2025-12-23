# Modules
import asyncio
from gpiozero import Button
import logging
from time import sleep

# Functions and variables
from payments import payment, return_to_screen
from qr import make_press_overlay, make_description, make_prompt_overlay, make_press_overlay
from var import pin_in, button_delay, inventory_delay, label, start_time

# Set up GPIO
buttons = [Button(btn, pull_up=False, hold_time=2) for btn in pin_in]
inventory_label = ["full", "empty"]

# A function that will check for each incoming pin whether there is a signal.
# A signal means that the tray is empty.
def get_inventory():
    logging.info(f"Obtaining inventory for pins {pin_in}")
    init_inventory = []
    for btn in buttons:
        global inventory
        inventory = init_inventory.append(btn.value)
        tray = buttons.index(btn)
        item = btn
        if btn.value ==1:
            logging.info(f"Tray {tray} at pin {pin_in[tray]} is {inventory_label[btn.value]}. Item: {label[tray]}")
        else:
            logging.debug(f"Tray {tray} at pin {pin_in[tray]} is {inventory_label[btn.value]}. Item: {label[tray]}")
    inventory = list(init_inventory)
    logging.debug(f"Inventory: {inventory}")

async def listener():
    make_prompt_overlay()
    logging.info(f"listening on pins {pin_in}")
    while True:
        detected = False
        for btn in buttons:
            if btn.is_pressed and inventory[buttons.index(btn)] == 0:
                logging.debug(f"{btn} HERE {btn.held_time}")
                detected = True
                global tray
                tray = buttons.index(btn)
                item = btn
                await asyncio.sleep(button_delay)
        if detected:
            logging.info(f"Pin {pin_in[tray]} pressed. Fetching payment for tray {tray} ({label[tray]})")
            logging.debug(item)
            make_press_overlay()
            make_description(tray)
            await payment(tray)
            return_to_screen()
            get_inventory()
            logging.info(f"listening on pins {pin_in}")
        # if an event remains high for more than 0.5 sec it might
        # be counted again on the next loop. Likewise if an event
        # comes and goes before the next loop it will be missed.
        sleep(button_delay)