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
from waveshare_epd import epd3in7

epd = epd3in7.EPD()

def initialize():
	try:
		logging.debug("epd3in7")
		logging.info("Starting display init")
		epd.init(0)
	except IOError as e:
		logging.info(e)

def idlescreen():
	try:
		logging.info("2.read 4 Gray bmp file")
		#Idleimage = Image.open(os.path.join(picdir, '21UP480x280.bmp'))
		Idleimage = Image.open(os.path.join(picdir, '21UP_v.bmp'))
		#Idleimage =  Idleimage.transpose(Image.TRANSPOSE)
		epd.display_4Gray(epd.getbuffer_4Gray(Idleimage))
		epd.sleep()
	except IOError as e:
		logging.info(e)

def invoicescreen(qr_image):
	initialize()
	logging.debug("Initializing screen")
	#epd.display_4Gray(epd.getbuffer_4Gray(qr_image))
	epd.display_1Gray(epd.getbuffer(qr_image))
	logging.info("Showing invoicescreen")

def successscreen():
	logging.debug("Initializing fuccess screen")
	Successimage = Image.open(os.path.join(picdir, 'tick480x280.bmp'))
	epd.display_1Gray(epd.getbuffer(Successimage))
	logging.info("Showing success screen")

def failurescreen():
	logging.debug("Initializing failure screen")
	Successimage = Image.open(os.path.join(picdir, 'cross480x280.bmp'))
	epd.display_1Gray(epd.getbuffer(Successimage))
	logging.info("Showing failure screen")

def shutdown():
	logging.info("Shutting down screen")
	epd.init(0)
	epd.Clear(0xFF, 0)
	epd3in7.epdconfig.module_exit(cleanup=True)
	exit()