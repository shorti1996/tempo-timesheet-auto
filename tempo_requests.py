import requests

from config.settings import auth_header


def post(url, data=None, json=None, **kwargs):
    return requests.post(url, data=data, json=json, headers=auth_header, **kwargs)
