#!/usr/bin/env python3


import sys

import requests


client_id = sys.argv[1]
client_secret = sys.argv[2]
code = sys.argv[3]


params = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'redirect_uri': 'http://127.0.0.1',
}
token_url = 'https://www.googleapis.com/oauth2/v4/token'

response = requests.post(token_url, params=params)
tokens = response.json()

access_token = '{token_type} {access_token}'.format(**tokens)
refresh_token = tokens['refresh_token']


print('Access token:', access_token)
print('Refresh token:', refresh_token)
