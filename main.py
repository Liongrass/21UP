# Modules
import asyncio

# Functions and variables
from button import listener
from display import initalize, idlescreen, cleanup

####### MAIN ########

# The main function is run, showing the idle screen and waiting for button to be pressed

async def main():

	try:
		initalize()
		idlescreen()
		await listener()

	except KeyboardInterrupt:
		print("Keyboard Interrupt detected")
		cleanup()
		exit()


asyncio.run(main())