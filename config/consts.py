from pathlib import Path

from config.secrets import auth_token

api_url = 'https://api.tempo.io/core/3/'
api_url_worklogs = api_url + 'worklogs'

auth_header = {'Authorization': 'Bearer ' + auth_token}

root_path = Path(__file__).parent.parent
default_schedule_path = root_path / "schedule.json"
default_date_format = "%Y-%m-%d"
default_workweek_days = 5  # mon-fri