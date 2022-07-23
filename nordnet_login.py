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
    session.post(url, data = {'username': user, 'password': password})
    return session