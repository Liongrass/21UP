# 21UP

The new 21UP vending machine displays a Bolt11 invoice on the e-ink display when a button on the machine is pressed. When the invoice is paid it dispenses the requested can.

<img width="1018" height="509" alt="banner" src="https://github.com/user-attachments/assets/366ba7b7-83e2-4909-a4fc-3884f69ce163" />

Currently being implemented:
- The display now has all the basic functionality, but no success or failure messages

To be implemented:
- Keep listening for the button even when an invoice is currently pending.
- Cancel the current invoice when a button is pressed
- Make a setup.py file
- Speed up display
- Show success and failure messages on-screen
- Cleanup pins when program is exited

Bugs:

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
