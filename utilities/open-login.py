#!/usr/bin/env python3


import sys
import webbrowser

import requests


client_id = sys.argv[1]
project_id = sys.argv[2]


params = {
    'scope': 'https://www.googleapis.com/auth/sdm.service',
    'prompt': 'consent',
    'access_type': 'offline',
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': 'http://127.0.0.1',
}
login_url = f'https://nestservices.google.com/partnerconnections/{project_id}/auth'

request = requests.Request('GET', login_url, params=params).prepare()

webbrowser.open(request.url)
