import os
import json
import requests


class Vk:
    def __init__(self, access_token):
        self.access_token = access_token
        self.domain = 'https://api.vk.com/method'
        self.v = '5.107'

    def query(self, method, **params):
        prepared = ''
        for key, val in params.items():
            prepared += '&{}={}'.format(
                key, ','.join(val) if isinstance(val, list) else val
            )
        return requests.get(
            f'{self.domain}/{method}?{prepared}&v={self.v}&access_token={self.access_token}'
        )


secrets_path = os.path.join(os.path.dirname(__file__), 'secrets.json')

with open(secrets_path, mode='r', encoding='utf-8') as f:
    secrets = json.load(f)

vk = Vk(secrets['access_token'])

response = vk.query('friends.get', **{
    'order': 'random',
    'fields': ['nickname', 'city']
}).json()

friends = response['response']['items']
for friend in friends:
    print(friend)
