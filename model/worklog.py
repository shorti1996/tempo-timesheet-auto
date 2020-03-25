from dataclasses import dataclass, asdict

from config.consts import default_scrum_issue_key, default_time_spent_seconds, default_start_time, default_description, \
    default_author_account_id
from logic.calendarer import get_current_day, date_to_str


@dataclass
class WorklogPost:
    """Used to post a worklog to Tempo API"""
    issueKey: str
    timeSpentSeconds: int
    startDate: str
    startTime: str
    description: str
    authorAccountId: str

    @staticmethod
    def create_with_defaults(start_date=get_current_day()):
        return WorklogPost(default_scrum_issue_key,
                           default_time_spent_seconds,
                           start_date if isinstance(start_date, str) else date_to_str(start_date),
                           default_start_time,
                           default_description,
                           default_author_account_id)

    def __init__(self, issue_key, time_spent_seconds, start_date, start_time, description, author_account_id):
        self.issueKey = issue_key
        self.timeSpentSeconds = time_spent_seconds
        self.startDate = start_date
        self.startTime = start_time
        self.description = description
        self.authorAccountId = author_account_id

    def create_dict(self):
        return asdict(self)
