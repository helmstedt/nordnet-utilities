# This program logs into a Nordnet account and extracts transactions as a csv file.
# Handy for exporting to Excel with as few manual steps as possible.
import requests
from datetime import datetime
from datetime import date
from nordnet_configuration import accounts, transactions_startdate, transactions_filename
from nordnet_login import nordnet_login

session = requests.Session()
session = nordnet_login(session)
if session:
    today = date.today()
    enddate = datetime.strftime(today, '%Y-%m-%d')

    # A variable to store transactions before saving to csv
    transactions = ''

    # GET ACCOUNT TRANSACTION DATA #

    # Payload and url for transaction requests
    payload = {
        'locale': 'da-DK',
        'from': transactions_startdate,
        'to': enddate,
    }

    url = 'https://www.nordnet.dk/mediaapi/transaction/csv/filtered'

    firstaccount = True
    for portfolioname, id in accounts.items():
        payload['account_id'] = id
        data = session.get(url, params=payload)
        result = data.content.decode('utf-16')
        result = result.replace('\t', ';')
        result = result.splitlines()

        firstline = True
        for line in result:
            # For first account and first line, we use headers and add an additional column
            if line and firstline == True and firstaccount == True:
                transactions += line + ';' + 'Depotnavn' + '\n'
                firstaccount = False
                firstline = False
            # First lines of additional accounts are discarded
            elif line and firstline == True and firstaccount == False:
                firstline = False
            # Content lines are added
            elif line and firstline == False:
                # Fix because Nordnet sometimes adds one empty column too many
                if line.count(';') == 29:
                    line = line.replace('; ', ' ')
                transactions += line + ';' + portfolioname + '\n'

    # WRITE CSV OUTPUT TO FILE #
    with open(transactions_filename, "w", encoding='utf8') as fout:
        fout.write(transactions)
else:
    print('Not logged into Nordnet so cannot get transactions.')