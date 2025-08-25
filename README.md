# 21UP

The new 21UP vending machine displays a Bolt11 invoice on the e-ink display when a button on the machine is pressed. When the invoice is paid it dispenses the requested can.

Currently being implemented:
- Keep listening for the button even when an invoice is currently pending.
- Cancel the current when a button is pressed

To be implemented:
- Listen on multiple pins
- Configure individual prices for each tray
- Dispense on multiple pins
- The display

Prerequisites:

`sudo apt-get install python-RPi.gpio python3-RPi.gpio`

Installation:

`git clone https://github.com/Liongrass/21UP.git`
`cd 21UP`

`pip install requests websockets dotenv RPi.GPIO time`

Activate virtual environment:

`source env/bin/activate`

Run 21UP:

`python main.py`
