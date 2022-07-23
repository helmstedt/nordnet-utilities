# This program gets latest currency data from Nordnet and converts and saves to csv.
# Handy for exporting to Excel with as few manual steps as possible.
# The program does not rely on a Nordnet account.
import requests 
from nordnet_configuration import currencies_filename

session = requests.Session()

# Set NEXT cookie and header
url = 'https://www.nordnet.dk/markedet'
session.get(url)
session.headers['client-id'] = 'NEXT'

# Gets currency data
url = 'https://www.nordnet.dk/api/2/instrument_search/query/indicator?entity_type=CURRENCY&apply_filters=market_overview_group%3DDK_GLOBAL_MO'
currency = session.get(url)

currencies = currency.json()

# Generate CSV output of last value by looping through currencies
output = "navn;senest\n"
for currency in currencies['results']:
	name = currency['instrument_info']['name']
	price = str(currency['price_info']['last']['price'])
	price = price.replace(".",",")
	output += name + ";" + price + "\n"

# Write CSV output to file #
with open(currencies_filename, "w", encoding='utf8') as fout:
	fout.write(output)