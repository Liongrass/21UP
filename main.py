# Modules
import asyncio
import logging

# Functions and variables
from button import listener
from display import epd, idlescreen, initialize
from waveshare_epd import epd3in52b

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():
	try:
		logging.info("Starting up")
		initialize()
		idlescreen()
		await listener()

	except KeyboardInterrupt:
		logging.info("Shutting down screen")
		epd3in52b.epdconfig.module_exit(cleanup=True)
		exit()


asyncio.run(main())