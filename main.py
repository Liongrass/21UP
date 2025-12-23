# Modules
import asyncio
import logging

# Functions and variables
from barometer import get_barometrics
from button import get_inventory, listener
from display import check_display, initialize, shutdown #, epd
from screens import make_idlescreen
#from waveshare_epd import epd3in7

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():
	try:
		logging.info("Starting 21UP")
		get_barometrics()
		get_inventory()
		check_display()
		initialize()
		make_idlescreen()
		await listener()

	except KeyboardInterrupt:
		shutdown()

asyncio.run(main())