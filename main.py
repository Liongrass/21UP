# Modules
import asyncio

# Functions and variables
from button import listener

####### MAIN ########

# The main function is run, waiting for button to be pressed
asyncio.run(listener())
#async def main():
#	await asyncio.gather(asyncio.create_task(listener()))

#asyncio.run(main())