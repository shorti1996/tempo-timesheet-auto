import os
from pathlib import Path

from config.secrets import author_id_myself

default_scrum_issue_key = "CD-12"  # Scrum
default_time_spent_seconds = 30 * 60
default_start_time = "00:00:00"
default_description = "Daily"
default_author_account_id = author_id_myself

scheduler_post_daily_if_nothing_scheduled = True

