import tempo_requests
from config.settings import api_url_worklogs
from model.worklog import WorklogPost

test = WorklogPost.create_with_defaults("2020-03-16")
response = tempo_requests.post(api_url_worklogs, json=test.create_dict())
