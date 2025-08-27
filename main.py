# Modules
import asyncio

# Functions and variables
from button import listener

####### MAIN ########

# The main function is run, waiting for button to be pressed
asyncio.run(listener())

#asyncio.run(main())
'''
async def main():
    tasks = [
        asyncio.create_task(listenerA()),
        asyncio.create_task(listenerB()),
    ]
    #await asyncio.gather(*tasks)

asyncio.run(main())
'''

#listener()
#async def main():
#	await asyncio.gather(asyncio.create_task(listener()))

#async def main():
#    await asyncio.gather(asyncio.create_task(listener()), asyncio.create_task(payment()))

#asyncio.run(main())