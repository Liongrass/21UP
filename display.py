# Modules
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import sys
from time import sleep

# Functions and variables
from var import amount, libdir, picdir, label, fontA, fontB, unit, show_display
from waveshare_epd import epd3in7

epd = epd3in7.EPD()

def initialize():
	if show_display == True:
		logging.info("Display is enabled.")
		try:
			logging.debug("epd3in7")
			logging.info("Starting display init")
			epd.init(0)
		except IOError as e:
			logging.info(e)
	else:
			logging.info("Display is disabled.")

def idlescreen():
	if show_display == True:
		try:
			logging.info("2.read 4 Gray bmp file")
			global initial_img
			initial_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
			draw = ImageDraw.Draw(initial_img)
			for i in range(len(label)):
				draw.text((16, 205 + i*40), label[i], font = fontA)
				from button import inventory
				if inventory[i] == 0:
					draw.text((150, 205 + i*40), unit[i], font = fontA)
					draw.text((200, 205 + i*40), str(amount[i]), font = fontA)
				if inventory[i] == 1:
					draw.text((150, 205 + i*40), "Not Avail.", font = fontA)
			logging.debug(initial_img)
			epd.display_4Gray(epd.getbuffer_4Gray(initial_img))
			#epd.sleep()
		except IOError as e:
			logging.info(e)

def prompt_overlay():
	if show_display == True:
		prompt_img = initial_img
		draw = ImageDraw.Draw(prompt_img)
		draw.text((16, 205 + 6*40), "Make Selection Now", font = fontB)
		epd.display_1Gray(epd.getbuffer(prompt_img))
		logging.debug(prompt_img)
		logging.info("Overlaying prompt")
		epd.sleep()

def descriptionscreen(description_img): 
	if show_display == True:
		#initialize()
		epd.display_4Gray(epd.getbuffer_4Gray(description_img))
		#epd.display_1Gray(epd.getbuffer(description_img))
		logging.info("Showing descriptionscreen")

def press_overlay(press_img):
	if show_display == True:
		initialize()
		epd.display_1Gray(epd.getbuffer(press_img))
		logging.info("Overlaying press icon")


def invoicescreen(qr_image):
	if show_display == True:
			#epd.display_4Gray(epd.getbuffer_4Gray(qr_image))
			logging.info("Showing invoicescreen")
			epd.display_1Gray(epd.getbuffer(qr_image))
			logging.info("Showing invoicescreen")

def success_overlay(success_img):
	if show_display == True:
		logging.debug("Initializing success screen")
		epd.display_1Gray(epd.getbuffer(success_img))
		logging.info("Showing success screen")

def failure_overlay(failure_img):
	if show_display == True:
		logging.debug("Initializing failure screen")
		epd.display_1Gray(epd.getbuffer(failure_img))
		logging.info("Showing failure screen")

def errorscreen():
	if show_display == True:
		logging.debug("Initializing error screen")
		error_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
		draw = ImageDraw.Draw(error_img)
		string = "Error obtaining invoice.\n Is the server up?\n Check logs for details."
		draw.text((16, 205 + 40), string, font = fontA)
		epd.display_1Gray(epd.getbuffer(error_img))
		logging.info("Showing error screen")

def shutdown():
	if show_display == True:
		logging.info("Shutting down screen")
		epd.init(0)
		epd.Clear(0xFF, 0)
		epd3in7.epdconfig.module_exit(cleanup=True)