import stripe
import csv
from csv import writer, reader
from dotenv import load_dotenv
import os
# from dhooks import Webhook, Embed
# from main import invoice_id, invoice_url

# ENV FILES

api_key = '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'
webhook_url = os.getenv("DISCORD_WEBHOOK_PAID")
# Stripe API Key
stripe.api_key = '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'

with open('invoices.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        for row in csv_reader:
            customer_email = row[0]
            product_type = row[2]
            invoice_url = row[5]
            qty = row[3]
            invoice_id = row[4]


            invoiceSummary = stripe.Invoice.retrieve(invoice_id)
            status = invoiceSummary["status"]
            status = invoiceSummary["status"]


            if status == 'paid':
                print(f'{customer_email} has paid')
                # hook = Webhook(webhook_url)
                # embed = Embed(
                #     title='**Invoice Paid** :white_check_mark:',
                #     color=0xFEFEFE,
                #     timestamp='now'  # sets the timestamp to current time
                #     )
                # embed.add_field(name= '**Quantity**', value = qty, inline = True)
                # embed.add_field(name='**Product**', value = (f'{product_type} Proxies'), inline = True)
                # embed.add_field(name='**Email**', value = customer_email, inline = False)
                # embed.add_field(name='**Invoice Status**', value = status, inline = False)
                # embed.add_field(name='**Invoice URL**', value = f"[**[View Here]**]({invoice_url})", inline = False)
                # embed.set_footer(text='@exornus', icon_url='https://pbs.twimg.com/profile_images/1196496002489966592/N3dpBSGI_400x400.jpg')
                # embed.set_thumbnail(url='https://cdn.shopify.com/s/files/1/0273/6773/5366/products/ProxyProductImage_1024x1024@2x.png?v=1587495438')
                # hook.send(embed=embed)
            elif status == 'open':
                print(f'{customer_email} has not paid')


    

