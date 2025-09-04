# Modules
import logging
import os
import sys
from time import sleep

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# Functions and variables
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd3in52b

epd = epd3in52b.EPD()

UPForeverB = Image.open(os.path.join(picdir, '21UP_b.bmp'))
UPForeverR = Image.open(os.path.join(picdir, '21UP_r.bmp'))
blankscreen = Image.open(os.path.join(picdir, 'white.bmp'))

def initialize():
	try:
		logging.debug("epd3in52b")
		logging.info("Starting display init")
		epd.init()
	except IOError as e:
		logging.info(e)

def idlescreen():
	epd.display(epd.getbuffer(UPForeverB), epd.getbuffer(UPForeverR))
	logging.info("Showing idlescreen")

def invoicescreen(qr_image):
	epd.display(epd.getbuffer(qr_image), epd.getbuffer(blankscreen))
	logging.info("Showing invoicescreen")

def screencleanup():
	epd.Clear()
	epd3in52b.epdconfig.module_exit(cleanup=True)
	logging.info("Screen cleaned up")
