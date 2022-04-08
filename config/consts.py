from pathlib import Path

from config.secrets import tempo_auth_token

tempo_api_url = 'https://api.tempo.io/core/3/'
tempo_api_url_worklogs = tempo_api_url + 'worklogs'

tempo_auth_header = {'Authorization': 'Bearer ' + tempo_auth_token}

root_path = Path(__file__).parent.parent
default_schedule_path = root_path / "schedule.json"
default_report_output_path = root_path / "reports-output"
tex_files_output_path = Path(root_path / "output")
template_files_path = root_path / 'resources'
shared_path = Path("/shared")

default_date_format = "%Y-%m-%d"
month_only_date_format = "%Y-%m"
default_workweek_days = 5  # mon-fri

atlassian_api_url = 'https://jojomobile.atlassian.net/rest/api/2/'
atlassian_api_url_issue = atlassian_api_url + 'issue/'

# REPORTS
pivot_table_hours_header = "Godziny"
pivot_table_projects_header = "Projekty"
pivot_table_tasks_header = "Zadania"
pivot_table_total_name = "Suma końcowa"
order_number_template = '1/ Better Software Group S.A. - B/2020/%02d/01/%s'