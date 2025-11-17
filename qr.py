# from skimage import data, io, util
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from var import amount, label, picdir, unit

from display import descriptionscreen, invoicescreen, failurescreen, successscreen
from waveshare_epd import epd3in7

canvas_width = epd3in7.EPD_WIDTH
canvas_height = epd3in7.EPD_HEIGHT
#canvas = Image.new('1', (canvas_width, canvas_height), 'white')

#font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

def coordinates(img):
    x_center = (canvas_width - img.width) // 2
    y_center = (canvas_height - img.height) // 2
    global paste_box
    paste_box = (x_center, y_center+ 100, x_center + img.width, y_center + img.height + 100)
    logging.debug(f"QR coordinates {paste_box}")
    return paste_box

def make_description(tray):
    description_string = label[tray] + " selected!"
    amount_string = str(amount[tray]) + " " + unit[tray]
    description_img = Image.new('1', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(description_img)
    draw.text((40, 205), description_string, font = font24)
    draw.text((40, 445), amount_string, font = font24)
    descriptionscreen(description_img)

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
    qr_image = Image.new('1', (canvas_width, canvas_height), 'white')
    qr_image.paste(img, paste_box)
    logging.debug(qr_image)
    invoicescreen(qr_image)

def make_success_img():
    img = Image.open(os.path.join(picdir, 'tick100x100.bmp'))
    coordinates(img)
    success_img = Image.new('1', (canvas_width, canvas_height), 'white')
    coordinates(img)
    success_img.paste(img, paste_box)
    logging.debug(success_img)
    successscreen(success_img)

def make_failure_img():
    img = Image.open(os.path.join(picdir, 'cross100x100.bmp'))
    coordinates(img)
    failure_img = Image.new('1', (canvas_width, canvas_height), 'white')
    coordinates(img)
    failure_img.paste(img, paste_box)
    logging.debug(failure_img)
    failurescreen(failure_img)