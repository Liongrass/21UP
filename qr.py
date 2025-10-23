# from skimage import data, io, util
import logging
from PIL import Image
import qrcode

from display import invoicescreen
from waveshare_epd import epd3in7

# Not a typo. With this screen, the width is the height, and vice versa.
canvas_width = epd3in7.EPD_HEIGHT
canvas_height = epd3in7.EPD_WIDTH
canvas = Image.new('1', (canvas_width, canvas_height), 'white')

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
    x_center = (canvas_width - img.width) // 2
    y_center = (canvas_height - img.height) // 2
    paste_box = (x_center, y_center, x_center + img.width, y_center + img.height)
    logging.debug(f"QR coordinates {paste_box}")
    global qr_image
    qr_image = canvas
    qr_image.paste(img, paste_box)
    logging.debug(qr_image)
    invoicescreen(qr_image)