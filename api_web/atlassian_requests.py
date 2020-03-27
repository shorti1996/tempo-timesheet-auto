import requests
from requests.auth import HTTPBasicAuth

from config.secrets import atlassian_login, atlassian_auth_token


def atlassian_auth(func):
    def inner(*args, **kwargs):
        return func(*args, auth=HTTPBasicAuth(atlassian_login, atlassian_auth_token), **kwargs)

    return inner


# def get(url, params=None, **kwargs):
#     return requests.get(url, params=params, auth=HTTPBasicAuth(atlassian_login, atlassian_auth_token), **kwargs)
@atlassian_auth
def get(url, params=None, **kwargs):
    return requests.get(url, params, **kwargs)


def atlassian(f, *args, **kwargs):
    return f(*args, auth=HTTPBasicAuth(atlassian_login, atlassian_auth_token), **kwargs)
