import requests


class TempoRequest:
    def __init__(self, tempo_api_key):
        self.header = {'Authorization': 'Bearer ' + tempo_api_key}

    def get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, headers=self.header, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, headers=self.header, **kwargs)

    def tempo(self, f, *args, **kwargs):
        return f(*args, headers=self.header, **kwargs)
