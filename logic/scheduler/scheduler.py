import json
import re
from typing import Optional

from config.consts import default_schedule_path
from config.settings import default_start_time, default_author_account_id, scheduler_post_daily_if_nothing_scheduled
from logic.calendarer import get_current_day_string, is_day_workday, str_to_date
from model.worklog import WorklogPost


class Scheduler:
    def __init__(self, post_daily_if_nothing_scheduled=scheduler_post_daily_if_nothing_scheduled):
        self.json_str: Optional[str] = None
        self.schedule: Optional = None
        self.post_daily_if_nothing_scheduled = post_daily_if_nothing_scheduled

    def load_schedule_from_file(self, file: str = None):
        schedule_path = default_schedule_path if file is None else file
        with open(schedule_path) as json_file:
            self.json_str = json_file.read()

        self.schedule = json.loads(self.json_str)['schedule']

    def get_issues_for_day(self, the_day=get_current_day_string()):
        that_day_schedules = next(iter([day for day in self.schedule['days'] if day['date'] == the_day]), None)
        issues = []
        if that_day_schedules is not None:
            issues += [WorklogPost(issue['key'],
                                   Scheduler.parse_duration_string_to_seconds(issue['timeSpent']),
                                   the_day,
                                   default_start_time,
                                   issue['description'], default_author_account_id) for issue in that_day_schedules['issues']]

        if len(issues) == 0 and self.post_daily_if_nothing_scheduled:  # nothing scheduled
            if is_day_workday(str_to_date(the_day)):  # try to append daily if workday
                issues.append(WorklogPost.create_with_defaults(the_day))
        elif 'appendDefaultScrum' not in that_day_schedules \
                or ('appendDefaultScrum' in that_day_schedules and that_day_schedules['appendDefaultScrum']):
            issues.append(WorklogPost.create_with_defaults(the_day))

        return issues

    @staticmethod
    def parse_duration_string_to_seconds(duration_string):
        pattern = re.compile(r"(?:(\d+)(?:h))*(?:(\d+)(?:m))*")
        match = pattern.match(duration_string)
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 * 60 + minutes * 60
