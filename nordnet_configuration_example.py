import os
from dotenv import load_dotenv

load_dotenv()

# Nordnet user account credentials and accounts/portfolios names (choose yourself) and numbers.
# To get account numbers go to https://www.nordnet.dk/transaktioner and change
# between accounts. The number after "?accids%3D" in the URL is your account number.
# If you have only one account, your account number is 1.
user = os.getenv('nordnet_username', 'myusername')
password = os.getenv('nordnet_password', 'mypassword')
accounts = {
    'account one': '1',
    'account three': '3'
}
# Period start for transactions
transactions_startdate = '2013-01-01'
# File name for transactions file
transactions_filename = 'transactions.csv'
# File name for currencies file
currencies_filename = 'currencies.csv'

# List of shares to look up prices for.
# Format is: Name, Nordnet stock identifier
# See e.g. https://www.nordnet.dk/markedet/aktiekurser/16256554-novo-nordisk-b
# (identifier is 16256554)
# All shares must have a name (whatever you like). To get prices they must
# have a Nordnet identifier
sharelist = [
    ["Novo Nordisk B A/S", '16256554'],
    ["Tryg A/S", '16097566']
]
# Start date (start of historical price period)
prices_startdate = '2013-01-01'
# File name for prices file
prices_filename = 'stock_prices.csv'
