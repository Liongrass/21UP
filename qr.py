# from skimage import data, io, util
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
import random
from var import amount, label, picdir, unit, fontA, fontB, press_icondir, press_icons

from display import descriptionscreen, idlescreen, invoicescreen, failure_overlay, prompt_overlay, press_overlay, success_overlay
from waveshare_epd import epd3in7

canvas_width = epd3in7.EPD_WIDTH
canvas_height = epd3in7.EPD_HEIGHT
#canvas = Image.new('1', (canvas_width, canvas_height), 'white')

def canvas():
    canvas = Image.new('1', (canvas_width, canvas_height), 'white')
    return canvas

def coordinates(img):
    x_center = (canvas_width - img.width) // 2
    y_center = (canvas_height - img.height) // 2
    qr_offset = 100
    global paste_box
    paste_box = (x_center, y_center + qr_offset, x_center + img.width, y_center + img.height + qr_offset)
    logging.debug(f"QR coordinates {paste_box}")
    return paste_box

def make_press_overlay():
    img_path = random.choice(press_icons)
    logging.debug(f"Choosing {img_path} as press icon")
    img = Image.open(os.path.join(press_icondir, img_path))
    coordinates(img)
    press_img = canvas()
    press_img.paste(img, paste_box)
    logging.debug(press_img)
    press_overlay(press_img)

def make_description(tray):
    description_string = label[tray] + " selected!"
    amount_string = str(amount[tray]) + " " + unit[tray]
    global description_img
    description_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    #description_img = Image.new('1', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(description_img)
    draw.text((40, 205), description_string, font = fontB)
    draw.text((40, 445), amount_string, font = fontB)
    logging.debug(description_img)
    descriptionscreen(description_img)

def make_prompt_overlay():
    prompt_overlay()

def make_qrcode(invoice):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
        )
    qr.add_data(invoice["bolt11"])
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img = img.convert("1")
    coordinates(img)
    global qr_image
    qr_image = description_img
    #qr_image = Image.new('1', (canvas_width, canvas_height), 'white')
    qr_image.paste(img, paste_box)
    logging.debug(qr_image)
    invoicescreen(qr_image)

def make_success_overlay():
    img = Image.open(os.path.join(picdir, 'tick100x100.bmp'))
    coordinates(img)
    success_img = description_img
    #success_img = Image.new('1', (canvas_width, canvas_height), 'white')
    coordinates(img)
    success_img.paste(img, paste_box)
    logging.debug(success_img)
    success_overlay(success_img)

def make_failure_overlay():
    img = Image.open(os.path.join(picdir, 'cross100x100.bmp'))
    coordinates(img)
    failure_img = description_img
    #failure_img = Image.new('1', (canvas_width, canvas_height), 'white')
    coordinates(img)
    failure_img.paste(img, paste_box)
    logging.debug(failure_img)
    failure_overlay(failure_img)