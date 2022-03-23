import sys
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
import stripe
import os
import csv
from csv import writer, reader
from dotenv import load_dotenv
from dhooks import Webhook, Embed
load_dotenv()

api_key = os.getenv("STRIPE_API_KEY")
product_type_isp = os.getenv("ISP_PRICE_ID")
product_type_aio = os.getenv("AIO_PRICE_ID")
admin_order_webhook = os.getenv("DISCORD_WEBHOOK")

# No need to call this multiple times in your code, just call it once at the beginning (or from another file when you start to get more advanced)
# Think of it like this, once you set this equal, it gets saved in the "stripe" object. So there's no need to do it again unless  you change the api key
stripe.api_key = api_key

# skip first line i.e. read header first and then iterate over each row od csv as a list
with open('orderform_1.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            # There is no need for the code below, you've already opened the file above, you can just re-use the csv_reader variable
            # f = open('orderform_1.csv')
            # csv_f = csv.reader(f)

            # this was originally for row in csv_f, I changed it to csv_reader
            # Below, you begin to iterate over the file again, I think this was your issue. You are already under a for loop right now, 
            # Starting another for loop will cause issues like you're having
            # for row in csv_reader:
            
            # No need for parentheses around (row[0])
            customer_email = row[0]
            qty = row[1]
            # Note discord ID's are being recognized as 1.43156E+17, etc. Should be a way to change fix that by googling
            # Or it might only be happening on my pc idk
            discord_id = row[2]
            product_type = row[3]

            # Honestly having this code under a function is not the most beautiful looking code
            # Nothing wrong with, ik you're still figuring shit out. Functions are best used when you need to re-use certain blocks of code
            # In this case, you're only executing these pieces of code in one part of your application so there's really no need.
            # I'll leave them here for learning sake but its unecessary tbh, it will also save about 4 lines of code which later on when working with
            # larger apps, will add up to be very nice for code readability.

            def customerCreate():
                customer = stripe.Customer.create(
                    description=discord_id,
                    email=customer_email)
                id = customer["id"]
                print("Customer Successfully Created!")
                return id
            
            customer_id = customerCreate()  # Exports the customer_id from the customerCreate

            def invoiceCreate():
                if product_type == "ISP":
                    stripe.InvoiceItem.create(
                        customer=customer_id,
                        quantity=qty,
                        price=product_type_isp)   # Creates the invoice with the DC ISP product
                elif product_type == "AIO":
                    stripe.InvoiceItem.create(
                        customer=customer_id,
                        price=product_type_aio)   # Creates the invoice with the DC AIO product
                else:
                    print("Error, check order csv for product type")
                    sys.exit()
                invoice = stripe.Invoice.create(
                    customer=customer_id,
                    auto_advance="false",
                    collection_method="send_invoice",
                    days_until_due="1",
                )
                invoice_id = invoice["id"]  # Extracts the Invoice ID
                # Processes invoice so an email can be sent to the customer
                stripe.Invoice.finalize_invoice(invoice_id)
                return invoice_id
            # Exports the invoice_id from the invoiceCreate function
            invoice_id = invoiceCreate()

            def invoiceSummary():
                invoiceSummary = stripe.Invoice.retrieve(invoice_id)
                invoice_url = invoiceSummary["hosted_invoice_url"]
                print("Invoice Successfully Created!")
                return invoice_url
            # Exports the invoice_url from the invoiceSummary function
            invoice_url = invoiceSummary()
            print(invoice_url)

            def productInfo():
                if product_type == 'AIO':
                    productName = ("DC AIO Proxies")
                    return productName
                elif product_type == 'ISP':
                    productName = ("ISP Proxies")
                    return productName
                return productName
            product_name = productInfo

            def append_list_as_row():
                list_of_elem = [customer_email, customer_id,
                                product_type, qty, invoice_id, invoice_url, discord_id]
                # Open file in append mode
                with open('invoices.csv', 'a+', newline='') as write_obj:
                    # Create a writer object from csv module
                    csv_writer = writer(write_obj)
                    # Add contents of list as last row in the csv file
                    csv_writer.writerow(list_of_elem)
            
            append_list_as_row()
