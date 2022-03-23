import discord
import stripe
import os
import csv
from csv import writer

from dhooks import Webhook, Embed
import customerCreate



csv_row = customerCreate.stripeCreate()

print(csv_row)
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        append_list_as_row('invoices.csv', csv_row)



embed = Embed(
    description='**Thank you for your order :white_check_mark:**',
    color=0xFFFFF,
    timestamp='now'  # sets the timestamp to current time
    )



embed.set_footer(text='@exornus', icon_url='https://pbs.twimg.com/profile_images/1196496002489966592/N3dpBSGI_400x400.jpg')
embed.set_thumbnail(url='https://cdn.shopify.com/s/files/1/0273/6773/5366/products/ProxyProductImage_1024x1024@2x.png?v=1587495438')


from discord_webhooks import DiscordWebhooks

# Webhook URL for your Discord channel.
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/708148273436688437/Og5LZJDNzQpA0auLDKF6ZWWwLrhOoXIBrUOiUULB1H3ZjXaoWI78viWJGo39J7sGRNy2'

# Initialize the webhook class and attaches data.
webhook = DiscordWebhooks(WEBHOOK_URL)
webhook.set_content(title='**Thank you for your order :white_check_mark:**',color=0xFEFEFE)
webhook.add_field(name='**Product**', value = "50 DC AIO Proxies ", inline = True)
webhook.add_field(name='**Email**', value = "test1@dambomail.com", inline = True)
webhook.add_field(name='**Invoice**', value = "[**[Click Here]**](https://stackoverflow.com/questions/3905437/using-a-variable-outside-of-function-in-python)", inline = False)
webhook.set_footer(text='@exornus', icon_url='https://pbs.twimg.com/profile_images/1196496002489966592/N3dpBSGI_400x400.jpg')
webhook.set_thumbnail(url='https://cdn.shopify.com/s/files/1/0273/6773/5366/products/ProxyProductImage_1024x1024@2x.png?v=1587495438')
# Triggers the payload to be sent to Discord.
webhook.send()
