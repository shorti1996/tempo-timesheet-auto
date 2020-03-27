from pathlib import Path

from config.secrets import tempo_auth_token

tempo_api_url = 'https://api.tempo.io/core/3/'
tempo_api_url_worklogs = tempo_api_url + 'worklogs'

tempo_auth_header = {'Authorization': 'Bearer ' + tempo_auth_token}

root_path = Path(__file__).parent.parent
default_schedule_path = root_path / "schedule.json"
default_date_format = "%Y-%m-%d"
default_workweek_days = 5  # mon-fri

atlassian_api_url = 'https://jojomobile.atlassian.net/rest/api/2/'
atlassian_api_url_issue = atlassian_api_url + 'issue/'
