# Modules
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
import random

# Functions and variables
from var import amount, label, picdir, unit, fontA, fontB, press_icondir, press_icons
from display import display_overlay, display_screen, epd
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
    return paste_box

def make_idlescreen():
    global idle_img
    idle_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    display_screen(idle_img)
    draw = ImageDraw.Draw(idle_img)
    for i in range(len(label)):
        draw.text((16, 205 + i*40), label[i], font = fontA)
        from button import inventory
        if inventory[i] == 0:
            draw.text((150, 205 + i*40), unit[i], font = fontA)
            draw.text((200, 205 + i*40), str(amount[i]), font = fontA)
        if inventory[i] == 1:
            draw.text((150, 205 + i*40), "Not Avail.", font = fontA)
        display_overlay(idle_img)
    draw.text((16, 205 + 6*40), "Make Selection Now", font = fontB)
    logging.debug(idle_img)
    display_overlay(idle_img)
    epd.sleep()

def make_press_overlay():
    img_path = random.choice(press_icons)
    logging.debug(f"Choosing {img_path} as press icon")
    img = Image.open(os.path.join(press_icondir, img_path))
    logging.debug(f"Overlay coordinates: {coordinates(img)}")
    overlay_img = canvas()
    overlay_img.paste(img, paste_box)
    logging.debug(overlay_img)
    logging.debug("Showing press overlay")
    display_overlay(overlay_img)

def make_description():
    global description_img
    description_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    logging.debug(description_img)
    logging.debug("Showing empty description screen")
    display_screen(description_img)

def make_qrcode(tray, t, invoice):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3.9,
        border=1,
        )
    qr.add_data(invoice["bolt11"].upper())
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img = img.convert("1")
    qr_coordinates = coordinates(img)
    logging.debug(f"QR coordinates: {qr_coordinates}")
    global qr_width
    qr_width = img.width
    logging.debug(f"QR Code Width: {qr_width}")
    
    qr_image = description_img
    qr_image.paste(img, paste_box)
    display_overlay(qr_image)

    description_string = label[tray]
    amount_string = str(unit[tray]) + " " + str(amount[tray])
    temperature_string = str(t) + " °C"
    
    draw = ImageDraw.Draw(qr_image)
    draw.text((qr_coordinates[0], qr_coordinates[2] - 6), description_string, anchor="la", font = fontB)
    display_overlay(qr_image)
    draw.text((qr_coordinates[0], qr_coordinates[3]), temperature_string, anchor="la", font = fontA)
    display_overlay(qr_image)
    draw.text((qr_coordinates[2], qr_coordinates[3]), amount_string, anchor="ra", font = fontB)

    logging.debug(qr_image)
    logging.debug("Showing QR overlay")
    display_overlay(qr_image)

def make_success_overlay():
    orig_img = Image.open(os.path.join(picdir, 'tick200x200.bmp'))
    img = orig_img.resize((qr_width, qr_width))
    logging.debug(f"Overlay coordinates: {coordinates(img)}")
    overlay_img = description_img
    overlay_img.paste(img, paste_box)
    logging.debug(overlay_img)
    logging.debug("Showing success overlay")
    display_overlay(overlay_img)

def make_failure_overlay():
    orig_img = Image.open(os.path.join(picdir, 'cross200x200.bmp'))
    img = orig_img.resize((qr_width, qr_width))
    logging.debug(f"Overlay coordinates: {coordinates(img)}")
    overlay_img = description_img
    overlay_img.paste(img, paste_box)
    logging.debug(overlay_img)
    logging.debug("Showing failure overlay")
    display_overlay(overlay_img)

def make_errorscreen():
    img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    draw = ImageDraw.Draw(img)
    string = "Error obtaining invoice.\n Is the server up?\n Check logs for details."
    draw.text((16, 205 + 40), string, font = fontA)
    logging.debug(img)
    logging.info("Showing error screen")
    display_screen(img)