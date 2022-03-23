import json
import_string = '''
{
  "keys": [
    {
      "stripeKey": "sk_test_bf9hNAbfBUHFATm2gMKHXmga003p53h5a7",
      "discordWebhook": "https://canary.discordapp.com/api/webhooks/708148273436688437/Og5LZJDNzQpA0auLDKF6ZWWwLrhOoXIBrUOiUULB1H3ZjXaoWI78viWJGo39J7sGRNy2",
      "empty": "empty"
   }
   ],
   "items": [
     {
       "ISP": "price_1HO9s0JBtaKem9eNVRCC4PeU",
       "Empty 1": "",
       "Empty 2": ""
     }
   ]
  }
'''
config = json.loads(import_string)

