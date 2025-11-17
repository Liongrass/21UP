# Modules
import logging
import os
import sys
from time import sleep

# Functions and variables
from PIL import Image, ImageDraw, ImageFont
from var import libdir, picdir
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
		Idleimage = Image.open(os.path.join(picdir, '21UP_v.bmp'))
		epd.display_4Gray(epd.getbuffer_4Gray(Idleimage))
		epd.sleep()
	except IOError as e:
		logging.info(e)

def descriptionscreen(description_img): 
	try:
		initialize()
		epd.display_1Gray(epd.getbuffer(description_img))
		logging.info("Showing descriptionscreen")
	except IOError as e:
		logging.info(e)

def invoicescreen(qr_image):
	try:
		#epd.display_4Gray(epd.getbuffer_4Gray(qr_image))
		epd.display_1Gray(epd.getbuffer(qr_image))
		logging.info("Showing invoicescreen")
	except IOError as e:
		logging.info(e)

def successscreen(success_img):
	logging.debug("Initializing success screen")
	epd.display_1Gray(epd.getbuffer(success_img))
	logging.info("Showing success screen")

def failurescreen(failure_img):
	logging.debug("Initializing failure screen")
	epd.display_1Gray(epd.getbuffer(failure_img))
	logging.info("Showing failure screen")

def shutdown():
	logging.info("Shutting down screen")
	epd.init(0)
	epd.Clear(0xFF, 0)
	epd3in7.epdconfig.module_exit(cleanup=True)
	exit()