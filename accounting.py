# Modules
import csv
import logging
import os


# Functions and variables
from var import amount, display_expiry, suceess_screen_expiry, expiry, label, lnbits_server, memo_str, pin_out, show_display, unit, x_api_key
#from var import amount, display_expiry, suceess_screen_expiry, expiry, label, lnbits_server, memo_str, pin_out, show_display, unit, x_api_key

fieldnames = ['settled', 'date', 'tray', 'item', 'price', 'currency', 'time_to_pay', 'payment_hash']

def check_csv():
    exists = os.path.isfile('pic/sales.csv')
    if exists == False:
        logging.debug("No existing CSV found. Creating new one.")
        create_csv()
    else:
        logging.debug("CSV already exists. Continuing.")


def create_csv():
    with open('pic/sales.csv', mode='w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

def amend_csv(settled, invoice_created, tray, invoice_paid, payment_hash):
    if invoice_paid == invoice_created:
        time_to_pay = "N/A"
    else:
        time_to_pay = invoice_paid - invoice_created
    data = {'settled': settled,
            'date': invoice_created,
            'tray': tray,
            'item': label[tray],
            'price': amount[tray],
            'currency': unit[tray],
            'time_to_pay': time_to_pay,
            'payment_hash': payment_hash}
    with open('pic/sales.csv', mode='a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(data)

#def write_csv(filename, data):
#    fieldnames = ['title', 'minsat', 'maxsat', 'comment', 'id', 'lnurl']
#    with open('csv/'+filename, mode='w') as csv_file:
#        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#        csv_writer.writeheader()
#        for row in data:
#            csv_writer.writerow(row)