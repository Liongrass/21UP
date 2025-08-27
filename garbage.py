
# This function checks whether a recently generated invoice has been paid
def check_invoice(invoice):
    try:
        check_invoice_url = (url_base + "/" + invoice["payment_hash"])
        check_invoice = requests.get(check_invoice_url, headers=headers)
        check = check_invoice.json()
        print("Paid:", check["paid"])
    except Exception as e:
        print("Exception thrown while trying to check invoice" + e)
        return

def buttonEventHandler_rising(channel):
    print(f"GPIO signal detected on pin {channel}.")
    asyncio.create_task(payment())

async def listener():
    setupGPIO()
    print("Listening for a button press")
    try:
        for ch in pin_list:
            GPIO.add_event_detect(ch, GPIO.RISING, callback=buttonEventHandler_rising, bouncetime=500)
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup finished.")