# This program extracts historical stock prices from Nordnet and saves to CSV.
# Does not require a login to Nordnet.
import requests
from datetime import datetime
from datetime import date
import os
from nordnet_configuration import sharelist, prices_startdate, prices_filename

# VISIT NORDNET #
session = requests.Session()
url = 'https://www.nordnet.dk/markedet'
session.get(url)
# Update headers
session.headers['client-id'] = 'NEXT'
session.headers['sub-client-id'] = 'NEXT'

# A variable to store historical prices before saving to csv	
finalresult = ""
finalresult += '"date";"price";"instrument"' + '\n'

# LOOP TO REQUEST HISTORICAL PRICES  #
for share in sharelist:
    url = "https://www.nordnet.dk/api/2/instruments/historical/prices/" + share[1]
    payload = {"from": prices_startdate, "fields": "last"}
    data = session.get(url, params=payload)
    jsondecode = data.json()
    
    # Sometimes the final date is returned twice. A list is created to check for duplicates.
    datelist = []
    if jsondecode[0]['prices']:
        for value in jsondecode[0]['prices']:
            if 'last' in value:
                price = str(value['last'])
            elif 'close_nav' in value:
                price = str(value['close_nav'])
            price = price.replace(".",",")
            date = datetime.fromtimestamp(value['time'] / 1000)
            date = datetime.strftime(date, '%Y-%m-%d')
            # Only adds a date if it has not been added before
            if date not in datelist:
                datelist.append(date)
                finalresult += '"' + date + '"' + ";" + '"' + price + '"' + ";" + '"' + share[0] + '"' + "\n"

# WRITE CSV OUTPUT TO FILE #			
with open(prices_filename, "w", newline='', encoding='utf8') as fout:
	fout.write(finalresult)