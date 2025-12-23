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
    logging.debug(f"QR coordinates {paste_box}")
    logging.debug(f"Image width: {img.width}. Image height: {img.height}")
    return paste_box

def make_idlescreen():
    global idle_img
    idle_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    draw = ImageDraw.Draw(idle_img)
    for i in range(len(label)):
        draw.text((16, 205 + i*40), label[i], font = fontA)
        from button import inventory
        if inventory[i] == 0:
            draw.text((150, 205 + i*40), unit[i], font = fontA)
            draw.text((200, 205 + i*40), str(amount[i]), font = fontA)
        if inventory[i] == 1:
            draw.text((150, 205 + i*40), "Not Avail.", font = fontA)
    logging.debug(idle_img)
    display_screen(idle_img)

def make_prompt_overlay():
    prompt_img = idle_img
    draw = ImageDraw.Draw(prompt_img)
    draw.text((16, 205 + 6*40), "Make Selection Now", font = fontB)
    logging.info("Overlaying prompt")
    display_overlay(prompt_img)
    epd.sleep()

def make_press_overlay():
    img_path = random.choice(press_icons)
    logging.debug(f"Choosing {img_path} as press icon")
    img = Image.open(os.path.join(press_icondir, img_path))
    coordinates(img)
    overlay_img = canvas()
    overlay_img.paste(img, paste_box)
    logging.debug(overlay_img)
    logging.debug("Showing press overlay")
    display_overlay(overlay_img)

def make_description(tray):
    description_string = label[tray] + " selected!"
    amount_string = str(amount[tray]) + " " + unit[tray]
    global description_img
    description_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    #description_img = Image.new('1', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(description_img)
    draw.text((48, 220), description_string, font = fontB)
    draw.text((225, 455), amount_string, anchor="rs", font = fontB)
    logging.debug(description_img)
    logging.debug("Showing description screen")
    display_screen(description_img)

def make_qrcode(t, invoice):
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
    coordinates(img)
    global qr_image
    qr_image = description_img
    #qr_image = Image.new('1', (canvas_width, canvas_height), 'white')
    qr_image.paste(img, paste_box)
    logging.debug(qr_image)
    logging.debug("Showing QR overlay")
    display_overlay(qr_image)

def make_success_overlay():
    img = Image.open(os.path.join(picdir, 'tick175x175.bmp'))
    coordinates(img)
    overlay_img = description_img
    #success_img = Image.new('1', (canvas_width, canvas_height), 'white')
    #coordinates(img)
    overlay_img.paste(img, paste_box)
    logging.debug(overlay_img)
    logging.debug("Showing success overlay")
    display_overlay(overlay_img)

def make_failure_overlay():
    img = Image.open(os.path.join(picdir, 'cross175x175.bmp'))
    coordinates(img)
    overlay_img = description_img
    #failure_img = Image.new('1', (canvas_width, canvas_height), 'white')
    #coordinates(img)
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