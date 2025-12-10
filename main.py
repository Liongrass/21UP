# Modules
import asyncio
import logging

# Functions and variables
from button import get_inventory, listener
from display import epd, idlescreen, initialize, shutdown
from waveshare_epd import epd3in7
from var import show_display

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():
	try:
		logging.info("Starting up")
		get_inventory()
		if show_display == True:
			logging.info("Display is enabled.")
			initialize()
			idlescreen()
		else:
			logging.info("Display is disabled.")
		await listener()

	except KeyboardInterrupt:
		if show_display == True:
			shutdown()
		exit()

asyncio.run(main())