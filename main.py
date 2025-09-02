# Modules
import asyncio
import logging

# Functions and variables
from button import listener
from display import idlescreen, initalize, screencleanup

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():
	try:
		logging.info("Starting up")
		initalize()
		idlescreen()
		await listener()

	except KeyboardInterrupt:
		logging.info("Keyboard Interrupt detected")
		screencleanup()
		exit()


asyncio.run(main())