from nordnet_configuration import user, password

def nordnet_login(session):
    # Setting cookies prior to login by visiting login page
    url = 'https://www.nordnet.dk/logind'
    session.get(url)

    # Update headers for login
    session.headers['client-id'] = 'NEXT'
    session.headers['sub-client-id'] = 'NEXT'

    # Actual login
    url = 'https://www.nordnet.dk/api/2/authentication/basic/login'
    login = session.post(url, data = {'username': user, 'password': password})
    # Success
    if login.status_code == 200:
        return session
    else:
        print(f'Login to Nordnet failed with status code {login.status_code}. The response was:')
        print(login.text)
        print('Please check that you have correctly set up nordnet_configuration.py and enabled username/password logins on Nordnet')
        return False