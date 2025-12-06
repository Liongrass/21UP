# Modules
import asyncio
import logging

# Functions and variables
from button import listener
from display import epd, idlescreen, initialize, shutdown
from waveshare_epd import epd3in7
from var import show_display

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():
	try:
		logging.info("Starting up")
		if show_display == True:
			initialize()
			idlescreen()
		await listener()

	except KeyboardInterrupt:
		if show_display == True:
			shutdown()
		exit()


asyncio.run(main())