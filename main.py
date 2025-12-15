# Modules
import asyncio
import logging

# Functions and variables
from button import get_inventory, listener
from display import epd, idlescreen, initialize, shutdown
from waveshare_epd import epd3in7

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():
	try:
		logging.info("Starting up")
		get_inventory()
		initialize()
		idlescreen()
		await listener()

	except KeyboardInterrupt:
		shutdown()
		exit()

asyncio.run(main())