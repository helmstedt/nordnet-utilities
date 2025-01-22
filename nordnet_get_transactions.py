# This program logs into a Nordnet account and extracts transactions as a csv file.
# Handy for exporting to Excel with as few manual steps as possible.
from datetime import datetime, date
import csv
import base64
from nordnet_configuration import accounts, transactions_startdate, transactions_filename
from nordnet_login import nordnet_login

session = nordnet_login()
if session:
    today = date.today()
    enddate = datetime.strftime(today, '%Y-%m-%d')

    # A variable to store transactions before saving to csv
    transactions = ''

    # GET ACCOUNT TRANSACTION DATA #
    firstaccount = True
    for portfolioname, id in accounts.items():
        url = f'https://api.prod.nntech.io/transaction/transaction-and-notes/v1/transactions/csv/filter?accids={id}&fromDate={transactions_startdate}&toDate={enddate}&sort=ACCOUNTING_DATE&sortOrder=DESC&includeCancellations=false'
        data = session.get(url)
        response_bytes = data.json()['bytes']
        decoded_bytes = base64.b64decode(response_bytes)
        result = decoded_bytes.decode('utf-16')
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