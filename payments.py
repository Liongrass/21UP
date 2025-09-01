# Modules
import requests
import json
import asyncio
import websockets

# Functions and variables
from dispense import trigger
from var import x_api_key, lnbits_server, memo_str, expiry, label, amount, unit, pin_out

####### VARIABLES ########

url_base = "https://" + lnbits_server + "/api/v1/payments"
ws_base = "wss://" + lnbits_server + "/api/v1/ws/"

##################################

def params(tray):
        params = {"out": False,
                  "amount": amount[tray],
                  "unit": unit[tray],
                  "memo": memo_str.format(label=label[tray],amount=amount[tray],unit=unit[tray]),
                  "expiry": expiry}
        # print(params)
        return params

headers = {"X-Api-Key" : x_api_key,
           "Content-type" : "application/json"}

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
        while True:
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
    print(f"Getting invoice for tray {tray} ({label[tray]})")
    get_invoice(params, headers, tray)
    try:
        await asyncio.wait_for(listen_for_payment(ws_base, x_api_key, invoice, tray), timeout=expiry)
    except asyncio.TimeoutError:
        print("Invoice expired")
    finally:
        print("Cycle complete")