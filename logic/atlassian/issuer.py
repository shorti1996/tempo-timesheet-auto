import json

from api_web.atlassian_requests import get
from config.consts import atlassian_api_url_issue


class Issuer:
    @staticmethod
    def get_issue(issue_key):
        response = get(atlassian_api_url_issue + issue_key)
        return json.loads(response.content)
