import requests

from config.consts import tempo_auth_header


def get(url, params=None, **kwargs):
    return requests.get(url, params=params, headers=tempo_auth_header, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return requests.post(url, data=data, json=json, headers=tempo_auth_header, **kwargs)


def tempo(f, *args, **kwargs):
    return f(*args, headers=tempo_auth_header, **kwargs)
