# Modules
import sys
import os
from time import sleep

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# Functions and variables
from waveshare_epd import epd3in52b
from PIL import Image,ImageDraw,ImageFont

epd = epd3in52b.EPD()

UPForeverB = Image.open(os.path.join(picdir, '21UP_b.bmp'))
UPForeverR = Image.open(os.path.join(picdir, '21UP_r.bmp'))

def initalize():
	try:
		#logging.info("epd3in52b")  
		print("Starting display init")
		epd.init()
	except IOError as e:
		logging.info(e)

def cleanup():
	try:
		epd.Clear()
		epd3in52b.epdconfig.module_exit(cleanup=True)
	finally:
		return None

def idlescreen():
	epd.display(epd.getbuffer(UPForeverB), epd.getbuffer(UPForeverR))
	print("Showing idlescreen")