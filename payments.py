# Modules
import asyncio
import json
import logging
import requests
from time import sleep
import websockets

# Functions and variables
from dispense import trigger
from display import errorscreen, idlescreen, invoicescreen, shutdown
from qr import make_qrcode, make_success_img, make_failure_img
from var import amount, display_expiry, suceess_screen_expiry, expiry, label, lnbits_server, memo_str, pin_out, show_display, unit, x_api_key


####### VARIABLES ########

url_base = "https://" + lnbits_server + "/api/v1/payments"
ws_base = "wss://" + lnbits_server + "/api/v1/ws/"

##################################

def params(tray):
        params = {"out": False,
                  "amount": amount[tray],
                  "unit": unit[tray],
                  "memo": memo_str.format(label=label[tray],amount=amount[tray],unit=unit[tray]),
                  "expiry": expiry + display_expiry}
        logging.debug(f"Invoice parameters: {params}")
        return params

headers = {"X-Api-Key" : x_api_key,
           "Content-type" : "application/json"}

# This function generates an invoice through the LNbits API and returns only the Bolt11 invoice
def get_invoice(params, headers, tray):
    try:
        invoice_request = requests.post(url_base, json=params(tray), headers=headers)
        invoice_request.raise_for_status()
        global invoice
        invoice = invoice_request.json()
        logging.debug(f"{invoice}")
        logging.info(invoice["bolt11"])
        if show_display == True:
            make_qrcode(invoice)
    except Exception as e:
        logging.debug(f"ERROR {e}")
        return

# This function connects to the LNbits websockets, checks for incoming payments and verifies whether they belong to the most recent invoice
async def listen_for_payment(ws_base, x_api_key, invoice, tray):
    async with websockets.connect(ws_base + x_api_key) as websocket:
        logging.debug(f"Connected to {ws_base}")
        logging.info(f"Waiting for payment: {invoice['amount']/1000} sat")
        while True:
            try:
                response_str = await websocket.recv()
                response = json.loads(response_str)
                if response["payment"]["payment_hash"] == invoice["payment_hash"]:
                    if show_display == True:
                        make_success_img()
                    logging.info(f"Payment received. Dispensing {label[tray]} (tray {tray}). Payment hash: " + response['payment']['payment_hash'])
                    trigger(pin_out, tray)
                    sleep(suceess_screen_expiry)
                    if show_display == True:
                        idlescreen()
                    break
                else:
                    logging.debug(f"Ignoring incoming payment for {response['payment']['amount']/1000} sat. Payment hash does not belong to invoice")
            except websockets.exceptions.ConnectionClosed as e:
                logging.debug(f"Connection closed: {e}")
                break
            except json.JSONDecodeError as e:
                logging.debug(f"Failed to decode JSON: {e}")
                continue

# This is the main function. It will first get the invoice with get_invoice(), then evoke listen_for_payment(). If within sixty seconds the invoice is not paid, it will shut down.
async def payment(tray):
    logging.debug(f"Getting invoice for tray {tray} ({label[tray]})")
    get_invoice(params, headers, tray)
    try:
        invoice
        try:
            timeout = expiry + suceess_screen_expiry + display_expiry + 3
            await asyncio.wait_for(listen_for_payment(ws_base, x_api_key, invoice, tray), timeout=timeout)
        
        except asyncio.CancelledError:
            if show_display == True:
                shutdown()
            exit()
        except asyncio.TimeoutError:
            logging.info(f"Invoice expired after {expiry}s")
            logging.debug(f"Timeout reached after {timeout}s")
            if show_display == True:
                make_failure_img()
            sleep(display_expiry)
            if show_display == True:
                idlescreen()
        finally:
            logging.info("Cycle complete")
    except NameError:
        logging.error("Error obtaining invoice. Check logs for details.")
        if show_display == True:
            errorscreen()
            sleep(display_expiry)
            idlescreen()
            return