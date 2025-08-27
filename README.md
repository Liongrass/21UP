# 21UP

The new 21UP vending machine displays a Bolt11 invoice on the e-ink display when a button on the machine is pressed. When the invoice is paid it dispenses the requested can.

Currently being implemented:

To be implemented:
- Keep listening for the button even when an invoice is currently pending.
- Cancel the current invoice when a button is pressed
- Make a setup.py file
- The display
- Shutdown logic

Bugs:
- When interrupting the process for the first time, it registers as a keyboard press

Prerequisites:

`sudo apt-get install python-RPi.gpio python3-RPi.gpio`

Installation:

`git clone https://github.com/Liongrass/21UP.git`

`cd 21UP`

`python -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

Run 21UP:

`python main.py`
