import requests
import json
import asyncio
import websockets
import os
from dotenv import load_dotenv

# Functions
from dispense import trigger, pin_out

####### VARIABLES ########

load_dotenv()

x_api_key = os.getenv("LNBITS_INVOICE_KEY")
lnbits_server = os.getenv("LNBITS_SERVER")
url_base = "https://" + lnbits_server + "/api/v1/payments"
ws_base = "wss://" + lnbits_server + "/api/v1/ws/"

amount = os.getenv("PRICE")
unit = os.getenv("UNIT")
memo = os.getenv("INVOICE_MEMO")
expiry = os.getenv("INVOICE_EXPIRY")

label = ["Coke", "21UP", "Beer"]
price = [10, 21, 42]

##################################

def params(tray):
        params = {"out": False,
                  "amount": price[tray],
                  "unit": unit,
                  "memo": f"One {label[tray]} from the 21UP machine. Thank you!",
                  "expiry": expiry}
        # print(params)
        return params

headers = {"X-Api-Key" : x_api_key,
           "Content-type" : "application/json"}

global stop_flag
stop_flag = True

def stop_process():
    global stop_flag
    stop_flag = False
    print("Setting Stop Flag")

# This function generates an invoice through the LNbits API and returns only the Bolt11 invoice
def get_invoice(params, headers, tray):
    try:
        invoice_request = requests.post(url_base, json=params(tray), headers=headers)
        global invoice
        invoice = invoice_request.json()
        #print(invoice)
        print(invoice["bolt11"])
    except Exception as e:
        print(e)
        return

# This function connects to the LNbits websockets, checks for incoming payments and verifies whether they belong to the most recent invoice
async def listen_for_payment(ws_base, x_api_key, invoice, tray):
    async with websockets.connect(ws_base + x_api_key) as websocket:
        print("Connected to " + ws_base)
        print(f"Waiting for payment: {invoice['amount']/1000} sat")
        while stop_flag == True:
            try:
                response_str = await websocket.recv()
                response = json.loads(response_str)
                if response["payment"]["payment_hash"] == invoice["payment_hash"]:
                    print(f"Payment received. Dispensing {label[tray]} (tray {tray}). Payment hash: " + response['payment']['payment_hash'])
                    trigger(pin_out, tray)
                    break
                else:
                    print(f"Ignoring incoming payment for {response['payment']['amount']/1000} sat. Payment hash does not belong to invoice")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                continue

# This is the main function. It will first get the invoice with get_invoice(), then evoke listen_for_payment(). If within sixty seconds the invoice is not paid, it will shut down.
async def payment(tray):
    global stop_flag
    stop_flag = True
    print(f"Getting invoice for tray {tray}")
    get_invoice(params, headers, tray)
    try:
        await asyncio.wait_for(listen_for_payment(ws_base, x_api_key, invoice, tray), timeout=60.0)
    except asyncio.TimeoutError:
        print("Invoice expired")
    finally:
        print("Cycle complete")