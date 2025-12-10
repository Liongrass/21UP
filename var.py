# Modules
from dotenv import load_dotenv
import json
import logging
import os
import sys
import time
import traceback
from PIL import ImageFont

##### VARIABLES #####

load_dotenv()

start_time = time.time()

x_api_key = os.getenv("LNBITS_INVOICE_KEY")
lnbits_server = os.getenv("LNBITS_SERVER", "send.laisee.org")

memo_str = os.getenv("MEMO_STRING", "Thank you for your purchase from 21UP!")
expiry = int(os.getenv("INVOICE_EXPIRY", 60))
display_expiry = int(os.getenv("DISPLAY_DELAY", 1))
suceess_screen_expiry = int(os.getenv("SUCCESS_SCREEN_EXPIRY", 5))

debuglevel = os.getenv("DEBUG_LEVEL", "INFO")

file_handler = logging.FileHandler('21UP.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

production = os.getenv("PRODUCTION", True).lower() in ('true', '1', 't')

logging.basicConfig(handlers=handlers, format='%(asctime)s %(levelname)s - %(message)s', level=debuglevel)
logging.info(f"Setting debug level at {debuglevel}")

##### TRAYS #####

tray0 = json.loads(os.environ['TRAY0'])
tray1 = json.loads(os.environ['TRAY1'])
tray2 = json.loads(os.environ['TRAY2'])
tray3 = json.loads(os.environ['TRAY3'])
tray4 = json.loads(os.environ['TRAY4'])
tray5 = json.loads(os.environ['TRAY5'])

label    = [tray0[0], tray1[0], tray2[0], tray3[0], tray4[0], tray5[0]]
amount   = [tray0[1], tray1[1], tray2[1], tray3[1], tray4[1], tray5[1]]
unit     = [tray0[2], tray1[2], tray2[2], tray3[2], tray4[2], tray5[2]]
pin_in   = [tray0[3], tray1[3], tray2[3], tray3[3], tray4[3], tray5[3]]
pin_out  = [tray0[4], tray1[4], tray2[4], tray3[4], tray4[4], tray5[4]]

logging.debug(f"Labels: {label}")
logging.debug(f"Amounts: {amount}")
logging.debug(f"Unit: {unit}")
logging.debug(f"Pin In: {pin_in}")
logging.debug(f"Pin Out: {pin_out}")

# pinOut=5  # CH1
# pinOut=6  # CH2
# pinOut=13 # CH3
# pinOut=16 # CH4
# pinOut=19 # CH5
# pinOut=20 # CH6
# pinOut=21 # CH7
# pinOut=26 # CH8

##### SYSTEM #####
button_delay = float(os.getenv("BUTTON_DELAY", 500)) / 1000
relay_duration = float(os.getenv("RELAY_DURATION", 500)) / 1000

##### DISPLAY #####

show_display = os.getenv("SHOWDISPLAY", True).lower() in ('true', '1', 't')

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

font_a = os.getenv("FONTA", "Font.ttc")
font_b = os.getenv("FONTB", "Rushfordclean.otf")
fontsize_a = int(os.getenv("FONTSIZEA", 24))
fontsize_b = int(os.getenv("FONTSIZEB", 32))

#font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
fontA = ImageFont.truetype(os.path.join(picdir, font_a), fontsize_a)
fontB = ImageFont.truetype(os.path.join(picdir, font_b), fontsize_b)