# 21UP

The new 21UP vending machine displays a Bolt11 invoice on the e-ink display when a button on the machine is pressed. When the invoice is paid it dispenses the requested can.

<img width="1018" height="509" alt="banner" src="https://github.com/user-attachments/assets/366ba7b7-83e2-4909-a4fc-3884f69ce163" />

Currently being implemented:
- Using partial refresh, the machine should show a quick notice when before an invoice is being fetched
- Make sure the "show display" setting actually works
- Get an inventory list at startup and every time an item is dispensed

To be implemented:
- Keep listening for the button even when an invoice is currently pending.
- Cancel the current invoice when a button is pressed
- Make a setup.py file
- Cleanup pins when program is exited
- Make use of LCD screen

Bugs:

- No bugs known. Please make an issue!

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

To run the machine first copy the example configuration file. Most importantly, a valid LNbits URL and invoice key need to be set.

`cp .env.example .env`

`python main.py`

## Deploying as a service

To make the code run on startup and restart after a crash, we are using the PM2 utility.

### Install PM2

Prerequisites:

`sudo apt install git make build-essential`

`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash`

`\. "$HOME/.nvm/nvm.sh"`

`nvm install 24`

`npm install -g pm2`

### Persist 21UP

`pm2 start /home/user/21UP/main.py --interpreter /home/user/21UP/env/bin/python --name 21UP --exp-backoff-restart-delay=100`

`pm2 startup`

This will give you a short command. Execute it to make 21UP run on startup.

Useful commands:

```
pm2 logs 21UP
pm2 list
pm2 monit
pm2 restart 21UP
```

### Further documentation

[E-ink display user manual](/docs/3.52inch-e-Paper_(B)-user-manual.pdf)

[E-ink display circuit schema](/docs/3.52inch_e-Paper_HAT.pdf)

[Display Guide](/docs/DISPLAY.md)

[Pin Inventory](/docs/pins.ods)
