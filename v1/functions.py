import sys
import stripe
import os
import csv
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import smtplib
import gmail
import json
from csv import writer, reader

stripe_key = 'sk_test_bf9hNAbfBUHFATm2gMKHXmga003p53h5a7'

def invoiceScript(stripe_key, discord_ID, customer_email, price_ID, qty, webhook_URL, file_name, invoice_count):
    stripe.api_key = stripe_key


    # Creates a customer for the invoice
    customer = stripe.Customer.create(
        description = discord_ID,
        email = customer_email)
    customer_ID = customer["id"]
    print(f"[{invoice_count}] Customer \'{customer_email}\' succesfully created!")

    # Assigns the invoice a product 
    product = stripe.InvoiceItem.create(
        customer = customer_ID,
        quantity = qty,
        price = price_ID)
    product_name = product["description"]
    print(f"[{invoice_count}] Product \'{product_name}\' assigned to \'{customer_email}\'")

    # Creates the invoice
    invoice = stripe.Invoice.create(
        customer = customer_ID,
        auto_advance = 'false',
        collection_method = 'send_invoice',
        days_until_due = '1')
    invoice_ID = invoice["id"]
    invoice_total = invoice["total"]
    print(f"[{invoice_count}] Invoice \'{invoice_ID}\' generated for \'{customer_email}\'")

    # Finalizes and sends order to customer_email
    stripe.Invoice.finalize_invoice(invoice_ID) # Processes invoice so an email can be sent to the customer
    stripe.Invoice.send_invoice(invoice_ID)
    invoiceSummary = stripe.Invoice.retrieve(invoice_ID)
    invoice_URL = invoiceSummary["hosted_invoice_url"]
    print(f"[{invoice_count}] Invoice sent to \'{customer_email}\'\n[{invoice_count}] Invoice URL: {invoice_URL}")



    if webhook_URL == '':
        print("[{invoice_count}] No webhook selected. Please add one into the config.py.")
    elif webhook_URL.startswith("https://") == False:
        print("[{invoice_count}] Error: Invalid Webhook URL")
    elif webhook_URL.startswith('https://') == True:
        
        # Since invoice_total saves as an int I need to conver it back into a float to display in webhook
        invoice_total_discord = invoice_total / 100

        


        webhook =  DiscordWebhook(
            url = webhook_URL
        )
        
        embed = DiscordEmbed(
            title = '**Invoice Successfully Created :white_check_mark:**',
            color = 0x5AFF5A
        )

        embed.set_author(
            name = '',
            url = '',
            icon_url = ''
        )

        # Adds a watermark for my twitter at the footer of the embed
        embed.set_footer(
            text = '@dambowastaken',
            icon_url = 'https://pbs.twimg.com/profile_images/1276720711311163392/me2_Mo3E_400x400.jpg'
        )
        
        # Sets a timestamp to the current time
        embed.set_timestamp()

        # Adds field 1
        embed.add_embed_field(
            name = '**Product:**',
            value = product_name,
            inline = True
        )
        
        # Adds field 2
        embed.add_embed_field(
            name = '**Quantity:**',
            value = qty,
            inline = True
        )
        
        # Adds field 3
        embed.add_embed_field(
            name = '**Order Total:**',
            value = (f'${invoice_total_discord}'),
            inline = False
        )


        # Adds field 4   
        embed.add_embed_field(
            name = '**Customer Email:**',
            value = customer_email,
            inline = False
        )

        # Adds the Full Embed into the webhook package
        webhook.add_embed(embed)
        # Sends the Webhook the the specified URL
        response = webhook.execute()
        print(f"[{invoice_count}] Webhook Response: {response}")



        csv_list = [customer_ID, customer_email, discord_ID, product_name, qty, invoice_ID, invoice_URL]
        with open(f'{file_name}.csv','a+', newline= '') as f:
            writer = csv.writer(f)
            writer.writerow(csv_list)
            if invoice_count >= 1:
                print(f'[{invoice_count}] File \'{file_name}\' updated')
            else:
                print(f'[{invoice_count}] File \'{file_name}\' created')

        print()
 
invoice_ID = 'in_1Hcx9jJBtaKem9eNdQNmsjYm'
webhook_URL = 'https://canary.discordapp.com/api/webhooks/708148273436688437/Og5LZJDNzQpA0auLDKF6ZWWwLrhOoXIBrUOiUULB1H3ZjXaoWI78viWJGo39J7sGRNy2'

def paymentVerification(stripe_key, invoice_ID, webhook_URL, verification_count):
    stripe.api_key = stripe_key
    invoiceSummary = stripe.Invoice.retrieve(invoice_ID)
    hasPaid = invoiceSummary["paid"]
    customer_email = invoiceSummary["customer_email"]
    amount_paid = invoiceSummary["amount_paid"]
    amount_due = invoiceSummary["amount_remaining"]



    if hasPaid == True:
        print(f'[{verification_count}] {invoice_ID} has been paid')

    
        
        amount_paid = amount_paid / 100
        amount_due = amount_due / 100
        
        
        
        webhook =  DiscordWebhook(
            url = webhook_URL
        )
        
        embed = DiscordEmbed(
            title = (f'**Invoice Paid :white_check_mark:**'),
            color = 0x5AFF5A
        )

        # Adds a watermark for my twitter at the footer of the embed
        embed.set_footer(
            text = '@dambowastaken',
            icon_url = 'https://pbs.twimg.com/profile_images/1276720711311163392/me2_Mo3E_400x400.jpg'
        )
        
        # Sets a timestamp to the current time
        embed.set_timestamp()
        
        # Adds field 1
        embed.add_embed_field(
            name = '**Amount Paid:**',
            value = (f'${amount_paid}'),
            inline = False
        )  

        # Adds field 2
        embed.add_embed_field(
            name = '**Amount Due:**',
            value = (f'${amount_due}'),
            inline = False
        )


        # Adds field 3
        embed.add_embed_field(
            name = '**Customer Email:**',
            value = customer_email,
            inline = False
        )

        # Adds the Full Embed into the webhook package
        webhook.add_embed(embed)
        # Sends the Webhook the the specified URL
        webhook.execute()
    

    return hasPaid
verification_count = 0


customer_email = 'test@dambomail.com'

def itemAllocation(qty):
    contents = []
    count = 0
    proxies = open("products/proxies.txt").read().splitlines()

    for proxy in proxies:
        if count == qty:
            count = 0
            break
        else:
            contents.append(proxy)
            count += 1
            proxies.remove(proxy)
    return contents


def gmailSender(customer_email, contents, qty, productType):
    sender_email = "exornusproxies@gmail.com"
    rec_email = customer_email
    password = "sximntdttjvalzvy"
    SUBJECT = (f"Your Proxies Are Here!")
    TEXT = (f"""
Thank you for your order. You can find your {qty} x {productType} below:

{contents}


Please feel free to join our discord with the link below:
https://discord.gg/b6vZQrZ
    """)
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login Success")
    server.sendmail(sender_email,rec_email, message)
    print(f'Email has been sent to {customer_email}')
# gmailSender(customer_email)


def stockPractice():
    portfolio = []
    stock = {}
    while True:
        userInput1 = input('Enter a symbol: ')
        if userInput1 != 'Quit':
            stock["symbol"] = userInput1
            userInput2 = float(input('Enter a value for the stock: '))
            stock["value"] = userInput2
            copy = stock.copy()
            portfolio.append(copy)
            

        elif userInput1 == 'Quit':
            for stock in portfolio:
                print(f"  {stock['symbol']} ${stock['value']}")
            break











customer_email = 'test@gmail.com'
customer_email = 'test@gmail.com'





def proxyDistributer(customer_email, qty):
    loadedProducts = []
    with open('proxylist.txt', 'r') as f:
        loadedProducts = f.readlines()
    proxyLeft = loadedProducts
    proxyInUse = []
    count = 0
    while count != qty:
        count += 1
        readProduct = proxyLeft[0]
        proxyInUse.append(readProduct)
        print(readProduct)
        del proxyLeft[0]
    return proxyInUse
proxyDistributer(customer_email, 5)
# contents = distributer('test@gmail.com', qty)


# gmailSender(customer_email, contents)








