import requests

from config.settings import auth_header


def get(url, params=None, **kwargs):
    return requests.get(url, params=params, headers=auth_header, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return requests.post(url, data=data, json=json, headers=auth_header, **kwargs)


def tempo(f, *args, **kwargs):
    return f(*args, headers=auth_header, **kwargs)
