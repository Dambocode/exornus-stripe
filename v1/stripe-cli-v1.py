import sys
import stripe
import os
import csv
from csv import writer, reader
from config import config
from functions import invoiceScript, paymentVerification
numberOfRows = 0
invoice_count = 0
verification_count = 0
print('=========================================================================================')
print('loading.........')

# Importing Variables from Config file
for keys in config['keys']:
    stripeKey = keys['stripeKey']
    webhook_URL = keys['discordWebhook']

for items in config['items']:
    product1 = items['ISP']


while True:
    home_selection = input('Please select one of the following options from the drop downs or type exit:\n1) Invoice Sender\n2) Payment Monitor\n')
    if home_selection == 'exit':
        break
    elif home_selection == '1':
        order_file = input("Enter the name of your orders file:\n")
        invoice_file = input("Enter a name for your invoice file that will be created:\n")
        with open(order_file, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    customer_email = row[0]
                    item_qty = row[1]
                    discord_name = row[2]

                    invoice_count = invoice_count + 1
                    invoiceScript(stripeKey, discord_name, customer_email, product1, item_qty, webhook_URL, invoice_file, invoice_count)
  
    elif home_selection == '2':
        invoice_file = input('Enter the name of your invoice file:\n')
        with open(invoice_file, 'r') as read_obj:
            csv_reader = reader(read_obj)
            invoice_list = []
            for row in csv_reader:
                invoice_ID = row[5]
                verification_count = verification_count + 1
                invoice_list.append(invoice_ID)
                
        while True:
            if invoice_list != []:
                for i in invoice_list:
                    numberOfRows = numberOfRows + 1
                    hasPaid = paymentVerification(stripeKey, i, webhook_URL, verification_count)
                    if hasPaid == True:
                        with open('paid_invoices.csv', 'a+', newline= '') as write_obj:
                            writer = csv.writer(write_obj)
                            writer.writerow(invoice_ID)
                        invoice_list.remove(i)

                    else:
                        print('Invoice not paid, checking next.')
            else:
                print('All invoices paid!')
                break