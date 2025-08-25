import requests
import json
import asyncio
import websockets
import os
from dotenv import load_dotenv

# Functions
from dispense import trigger, pinOut

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

##################################

params = {"out": False,
          "amount": amount,
          "unit": unit,
          "memo": memo,
          "expiry": expiry}

headers = {"X-Api-Key" : x_api_key,
           "Content-type" : "application/json"}

# This function generates an invoice through the LNbits API and returns only the Bolt11 invoice
def get_invoice(params, headers):
    try:
        invoice_request = requests.post(url_base, json=params, headers=headers)
        global invoice
        invoice = invoice_request.json()
        print(invoice["bolt11"])
    except Exception as e:
        print(e)
        return

# This function connects to the LNbits websockets, checks for incoming payments and verifies whether they belong to the most recent invoice
async def listen_for_payment(ws_base, x_api_key, invoice):
    async with websockets.connect(ws_base + x_api_key) as websocket:
        print("Connected to " + ws_base)
        print(f"Waiting for payment: {invoice['amount']} msat")
        while True:
            try:
                response_str = await websocket.recv()
                response = json.loads(response_str)
                
                if response["payment"]["payment_hash"] == invoice["payment_hash"]:
                    print("Payment received. Dispensing 21UP. Payment hash: " + response['payment']['payment_hash'])
                    trigger(pinOut)
                    break
                else:
                    print(f"Ignoring incoming payment for {response['payment']['amount']} msat. Payment hash does not belong to invoice")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                continue

# This is the main function. It will first get the invoice with get_invoice(), then evoke listen_for_payment(). If within sixty seconds the invoice is not paid, it will shut down.
async def payment():
    get_invoice(params, headers)
    try:
        await asyncio.wait_for(listen_for_payment(ws_base, x_api_key, invoice), timeout=60.0)
    except asyncio.TimeoutError:
        print("Invoice expired")
    finally:
        print("Dispensing complete")