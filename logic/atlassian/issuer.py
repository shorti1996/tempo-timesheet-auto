import json

import requests
from requests.auth import HTTPBasicAuth

from config.consts import atlassian_api_url_issue


class Issuer:
    def __init__(self, atlassian_login, jira_api_token):
        self.basic_auth = HTTPBasicAuth(atlassian_login, jira_api_token)

    def get_issue(self, issue_key):
        response = requests.get(atlassian_api_url_issue + issue_key, auth=self.basic_auth)
        return json.loads(response.content)

    def get(self, url, params=None, **kwargs):
        return requests.get(url, params, auth=self.basic_auth, **kwargs)
