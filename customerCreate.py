import sys
import stripe
import os
import csv
from csv import writer


def stripeCreate():


    productInput = input("Is this for DC AIO (a) or ISPs (b)?\n")


    f = open('orderform_1.csv')
    csv_f = csv.reader(f)

    for row in csv_f:
        customer_email = (row[0])
        qty = (row[1])
        discord_id = (row[2])
    print(f"""\

    discord id: {discord_id}
    quantity:   {qty}
    email:      {customer_email}
                    """)

# ---------------------------------------------------------------------------------------------------------
# Create Customer and get the customer ID
    stripe.api_key = "sk_test_bf9hNAbfBUHFATm2gMKHXmga003p53h5a7"
    customer = stripe.Customer.create(
        description = discord_id,
        email = customer_email
    )
    customer_id = customer["id"]
    print("Customer Successfully Created!")


# Create Invoice
    if productInput == "a":
        productName = (f"{qty} DC AIO Proxies")
        stripe.InvoiceItem.create(
        customer=customer_id,
        price='price_1HOA1lJBtaKem9eNq4Wr2uZF')   # DC AIO proxy priceID
    elif productInput == "b":
        productName = (f"{qty} ISP DC Proxies")
        stripe.InvoiceItem.create(
        customer=customer_id,
        price='price_1HOADXJBtaKem9eNbLmDxwbh'),   # ISP proxy priceID
  
    else:
        print("Invalid input. Please enter either \"a\" or \"b\"")
        sys.exit()
    
    invoice = stripe.Invoice.create(
        customer= customer_id,
        auto_advance = "false",
        collection_method = "send_invoice",
        days_until_due = "1",
    )

    invoice_id = invoice["id"]  # Extract the invoice ID from the 

    stripe.Invoice.finalize_invoice(invoice_id)

    invoiceSummary = stripe.Invoice.retrieve(invoice_id)

    invoice_url = invoiceSummary["hosted_invoice_url"]
    print("Invoice Successfully Created!")

    # with open('invoices.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['InvoiceID','Email', 'ProductName', 'InvoiceURL', 'DiscordID']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writerow({'InvoiceID': invoice_id,'Email': customer_email, 'ProductName': productName, "InvoiceURL": invoice_url, 'DiscordID': discord_id})
    print(f'\nInvoice ID: {invoice_id}\nCustomer ID: {customer_id}\nEmail: {customer_email}\nProduct Name: {productName}\nDiscord ID: {discord_id}\nInvoice URL: {invoice_url}')
    csv_row = [invoice_id,customer_id,customer_email,productName,discord_id,invoice_url]
    return csv_row
    








# Notify the customer via discord that their order has been processed

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Successfully connected to ', self.user)

#     embed = discord.Embed(color=0xffffff, title="__**Your order has been processed :white_check_mark:**__", description="Thank you for your order. You should recieve an invoice within the next hour. You can find your order details below.")
#     embed.add_field(name='Product', value=productName)
#     embed.add_field(name='Email', value=customer_email)
#     embed.set_footer(text='@exornus', icon_url='https://pbs.twimg.com/profile_images/1196496002489966592/N3dpBSGI_400x400.jpg')

#     guild = bot.get_guild(684905733480775711)
#     member = guild.get_member(143156387894132736)
#     if member is not None:
#         member.send(embed=embed)

# client = commands.Bot(command_prefix = '//')

# @client.event
# async def on_ready():
#         embed = discord.Embed(
#             title = '__**Your order is ready :white_check_mark:**__',
#             description =  'Thank you for your order. Your invoice details can be found below!'
#         )

#         embed.set_footer(text='@exornus', icon_url='https://pbs.twimg.com/profile_images/1196496002489966592/N3dpBSGI_400x400.jpg')
#         embed.set_thumbnail(url='https://cdn.shopify.com/s/files/1/0273/6773/5366/products/ProxyProductImage_1024x1024@2x.png?v=1587495438')
#         embed.add_field(name='Product', value = productName, inline = True)
#         embed.add_field(name='Email', value = customer_email, inline = True)

#         await client.message(embed=embed)