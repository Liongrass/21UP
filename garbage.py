
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