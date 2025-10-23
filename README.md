# 21UP

The new 21UP vending machine displays a Bolt11 invoice on the e-ink display when a button on the machine is pressed. When the invoice is paid it dispenses the requested can.

<img width="1018" height="509" alt="banner" src="https://github.com/user-attachments/assets/366ba7b7-83e2-4909-a4fc-3884f69ce163" />

Currently being implemented:
- The display now has all the basic functionality, but needs to go to sleep eventually, and be re-initialized before being refreshed
- Using partial refresh, the machine should show a quick notice when before an invoice is being fetched
- Display item name and price underneath the QR code

To be implemented:
- Keep listening for the button even when an invoice is currently pending.
- Cancel the current invoice when a button is pressed
- Make a setup.py file
- Cleanup pins when program is exited
- Main screen doesn't wake up

Bugs:

- Keyboard interrupt throws an error when invoice is open

## Prerequisites:

Enable the SPI interface:

`sudo raspi-config`

Then select Interfacing Options -> SPI -> Yes to enable the SPI interface

## Installation:

`git clone https://github.com/Liongrass/21UP.git`

`cd 21UP`

`python -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

## Run 21UP:

`python main.py`

### Further documentation

[E-ink display user manual](/docs/3.52inch-e-Paper_(B)-user-manual.pdf)

[E-ink display circuit schema](/docs/3.52inch_e-Paper_HAT.pdf)

[Display Guide](/docs/DISPLAY.md)
