import sys
import stripe
import os
import csv
from csv import writer, reader
from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("STRIPE_API_KEY")
# product_type_isp = os.getenv("ISP_PRICE_ID")
# product_type_aio = os.getenv("AIO_PRICE_ID")
# invoice_webhook_url = os.getenv("DISCORD_WEBHOOK_INVOICE")

# Stripe Key - THESE ARE NO LONGER ACTIVE FOR ANYONE TRYING TO USE THEM
stripe.api_key = ''
api_key = ''
# skip first line i.e. read header first and then iterate over each row od csv as a list
with open('orders.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
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
            discord_id = row[2]
            product_type = row[3]

            def customerCreate():
                customer = stripe.Customer.create(
                description = discord_id,
                email = customer_email)
                id = customer["id"]
                print("Customer Successfully Created!")
                return id
            customer_id = customerCreate()  # Exports the customer_id from the customerCreate
            def invoiceCreate():
                if product_type == "ISP":
                    stripe.api_key = api_key
                    stripe.InvoiceItem.create(
                    customer=customer_id,
                    quantity=qty,
                    price = 'price_1H0X6qJBtaKem9eNgqto9shV')   # Creates the invoice with the DC ISP product
                elif product_type == "AIO":
                    stripe.api_key = api_key
                    stripe.InvoiceItem.create(
                    customer=customer_id,
                    quantity=qty,
                    price = 'FIX')   # Creates the invoice with the DC AIO product
                else:
                    print("Error, check order csv for product type")
                    sys.exit()
                invoice = stripe.Invoice.create(
                    customer= customer_id,
                    auto_advance = "false",
                    collection_method = "send_invoice",
                    days_until_due = "1",
                )
                invoice_id = invoice["id"]  # Extracts the Invoice ID
                stripe.Invoice.finalize_invoice(invoice_id) # Processes invoice so an email can be sent to the customer
                stripe.Invoice.send_invoice(invoice_id)
                return invoice_id
            invoice_id = invoiceCreate()    # Exports the invoice_id from the invoiceCreate function
            def invoiceSummary():
                invoiceSummary = stripe.Invoice.retrieve(invoice_id)
                invoice_url = invoiceSummary["hosted_invoice_url"]
                print("Invoice Successfully Created!")
                return invoice_url
            invoice_url = invoiceSummary()  # Exports the invoice_url from the invoiceSummary function
            print(invoice_url)
            def productInfo():
                if product_type == 'AIO':
                    productName = ("DC AIO Proxies")
                    return productName
                elif product_type =='ISP':
                    productName = ("ISP Proxies")
                    return productName
                return productName
            product_name = productInfo   
            def append_list_as_row():
                list_of_elem = [customer_email,customer_id, product_type, qty, invoice_id, invoice_url, discord_id]
                # Open file in append mode
                with open('invoices.csv', 'a+', newline='') as write_obj:
                    # Create a writer object from csv module
                    csv_writer = writer(write_obj)
                    # Add contents of list as last row in the csv file
                    csv_writer.writerow(list_of_elem)
            append_list_as_row()
            # def invoiceDiscordLog():
            #     productDiscordName = (f'{qty} Monthly {product_type} Data Center Proxies')
            #     hook = Webhook('')

            #     embed = Embed(
            #         title='**New Invoice Created** :white_check_mark:',
            #         color=0xFEFEFE,
            #         timestamp='now'  # sets the timestamp to current time
            #         )
            #     embed.add_field(name='**Product**', value = productDiscordName, inline = True)
            #     embed.add_field(name='**Email**', value = customer_email, inline = True)
            #     embed.add_field(name='**Invoice Status**', value = f"[**[View Here]**]({invoice_url})", inline = False)
            #     embed.set_footer(text='@exornus', icon_url='https://pbs.twimg.com/profile_images/1196496002489966592/N3dpBSGI_400x400.jpg')
            #     embed.set_thumbnail(url='https://cdn.shopify.com/s/files/1/0273/6773/5366/products/ProxyProductImage_1024x1024@2x.png?v=1587495438')
            #     hook.send(embed=embed)
            # invoiceDiscordLog()
