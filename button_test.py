# Modules
import asyncio
from gpiozero import Button
import logging
from time import sleep

# Functions and variables
from payments import payment
from qr import make_description
from var import pin_in, button_delay

buttons = [Button(btn, pull_up=False, hold_time=0.1) for btn in pin_in]

async def listener():
	logging.info(f"listening on pins {pin_in}")
	while True:
		#held = False
		#global pressed
		#pressed = False
		global hodl
		hodl = 0
		for btn in buttons:
			if btn.is_pressed and btn.is_held:
				print(btn.held_time)
				hodl = btn.held_time
				#pressed = True
				tray = buttons.index(btn)
				btn.when_released = trigger(hodl, tray)

def trigger(hodl, tray):
	if hodl <= 2:
		print(f"button was pressed for {hodl} at tray {tray}")
		#pressed = False
		hodl = 0
		sleep(2)
	if hodl > 2 and hodl <= 10:
		print(f"button was held for {hodl} at tray {tray}")
		#pressed = False
		hodl = 0
		sleep(2)
	if hodl > 10:
		print(f"button was held for {hodl} at tray {tray}. Tray likely unavailable")
		hodl = 0
		sleep(2)


'''
            btn.when_held():
                detected = True
                global tray
                tray = buttons.index(btn)
                item = btn
        if detected:
            logging.info(f"Pin {pin_in[tray]} pressed. Fetching payment for tray {tray}")
            sleep(2)
'''


'''
def held(btn):
    btn.was_held = True
    print("button was held not just pressed")

def released(btn):
    if not btn.was_held:
        pressed()
    btn.was_held = False

def pressed():
    print("button was pressed not held")

btn = Button(2)

btn.when_held = held
btn.when_released = released
'''

async def main():
	try:
		logging.info("Starting up")
		await listener()

	except KeyboardInterrupt:
		shutdown()


asyncio.run(main())