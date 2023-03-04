# This program provides two examples of logging into a Nordnet account
# and extracting account performance as json data. One is based on standard
# intervals. The other is based on a user-defined interval.
# Storing and processing of returned data is left to you.
import requests
from nordnet_configuration import accounts
from nordnet_login import nordnet_login

session = requests.Session()
session = nordnet_login(session)
if session:
    accounts_list = [value for value in accounts.values()]

    ### Nordnet standard intervals (one month, three months, six months, ytd, 1 year, 3 years and 5 years)
    accounts_string = ','.join(accounts_list)
    url = 'https://www.nordnet.dk/api/2/accounts/' + accounts_string + '/returns/performance'
    period_options = ['m1','m3','m6','ty','y1','y3','y5']

    standard_graph_data = {}
    for period in period_options:
        params = {
            'period': period,
            'start_at_zero': False
        }
        graph = session.get(url, params=params)
        standard_graph_data[period] = graph.json()
    # Store and process graph_data as needed

    ### User defined date intervals
    start_date = '2019-01-30'   # Edit as needed
    end_date = '2019-05-14'    # Edit as needed
    user_defined_graph_data = {}
    for account in accounts_list:
        url = 'https://www.nordnet.dk/api/2/accounts/' + account + '/returns/performance'
        params = {
            'from': start_date,
            'to': end_date
        }
        user_defined_graph = session.get(url, params=params)
        user_defined_graph_data[account] = user_defined_graph.json()
    # Store and process user_defined_graph_data as needed
else:
    print('Not logged into Nordnet so cannot get performance graph.')