# 21UP

The new 21UP vending machine displays a Bolt11 invoice on the e-ink display when a button on the machine is pressed. When the invoice is paid it dispenses the requested can.

<img width="1018" height="509" alt="banner" src="https://github.com/user-attachments/assets/366ba7b7-83e2-4909-a4fc-3884f69ce163" />

Currently being implemented:
- The display now has all the basic functionality, but needs to go to sleep eventually, and be re-initialized before being refreshed
- Adjust invoice expiration time to accommodate for ~20s delay in display

To be implemented:
- Display item name and price underneath the QR code
- Keep listening for the button even when an invoice is currently pending.
- Cancel the current invoice when a button is pressed
- Make a setup.py file
- Speed up display
- Show success and failure messages on-screen
- Cleanup pins when program is exited

Bugs:

- Keyboard interrupt throws an error while invoice is open

Prerequisites:

Enable the SPI interface:

`sudo raspi-config`

Then select Interfacing Options -> SPI -> Yes to enable the SPI interface

Installation:

`git clone https://github.com/Liongrass/21UP.git`

`cd 21UP`

`python -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

Run 21UP:

`python main.py`
