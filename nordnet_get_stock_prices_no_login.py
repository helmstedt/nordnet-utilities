# Extracts historical stock prices from Nordnet and appends new data to a csv file.
# A maximum period of 5 years is available with daily resolution.
# Does not require login to Nordnet.
import requests
from datetime import datetime
from datetime import date
from nordnet_configuration import sharelist, prices_startdate, prices_filename
from os.path import exists
import csv

# Define fieldnames for csv and create list to store existing dates
fieldnames = ['date', 'instrument', 'high', 'low', 'open', 'last', 'volume']
datelist = []

# Prepare new CSV file if it doesn't exists
if not exists(prices_filename):
    with open(prices_filename, 'wt', encoding='utf-8', newline='') as prices_file:
        writer = csv.DictWriter(prices_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
# If it exists, get list of existing dates in order to only append new dates
else:
     with open(prices_filename, 'rt', encoding='utf-8') as prices_csv_file:
        reader = csv.DictReader(prices_csv_file, delimiter=';')
        for row in reader:
            date = row['date']
            if date not in datelist:
                datelist.append(date)

# Prepare session for requests
session = requests.Session()
session.headers['Origin'] = 'https://www.nordnet.dk'

# Loop to request historical prices and add to csv
with open(prices_filename, 'a', encoding='utf-8', newline='') as prices_csv_file:
    writer = csv.DictWriter(prices_csv_file, delimiter=';', fieldnames=fieldnames)
    for share in sharelist:
        instrument = share[0]
        url = 'https://api.prod.nntech.io/market-data/price-time-series/v2/period/YEAR_5/identifier/' + \
            share[1]
        params = {'resolution': 'DAY'}
        data = session.get(url, params=params)
        jsondecode = data.json()
        for day in jsondecode['pricePoints']:
            timestamp = day['timeStamp']
            date_datetime = datetime.fromtimestamp(timestamp / 1000)
            date = datetime.strftime(date_datetime, '%Y-%m-%d')
            if date not in datelist:
                row = {
                    'instrument': instrument,
                    'date': date,
                    'high': str(day['high']).replace(".", ","),
                    'low': str(day['low']).replace(".", ","),
                    'open': str(day['open']).replace(".", ","),
                    'last': str(day['last']).replace(".", ","),
                    'volume': str(day['volume']).replace(".", ","),
                }
                writer.writerow(row)