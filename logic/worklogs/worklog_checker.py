import json
from abc import abstractmethod

import tempo_requests
from config.consts import api_url_worklogs, default_workweek_days
from config.settings import default_scrum_issue_key
from logic.calendarer import get_current_day, get_week_days_str, date_to_str


class WorklogChecker:
    @property
    @abstractmethod
    def filter_predicate(self):
        ...

    def get_worklogs(self):
        response = tempo_requests.get(api_url_worklogs)
        results = json.loads(response.content)["results"]
        return results

    def get_issues(self):
        return filter(self.filter_predicate, self.get_worklogs())

    def get_worklogs_for_multiple_days(self, anchor_time=get_current_day(), days_num=default_workweek_days,
                                       days_str=None):
        if days_str is None:
            days_str = get_week_days_str(anchor_time, days_num)
        issues = self.get_issues()
        these_days_issues = [x for x in issues if x['startDate'] in days_str]
        return these_days_issues

    def get_worklogs_for_day(self, anchor_time=get_current_day()):
        return self.get_worklogs_for_multiple_days([date_to_str(anchor_time)])


class ScrumWorklogChecker(WorklogChecker):
    @property
    def filter_predicate(self):
        return lambda result: result['issue']['key'] == default_scrum_issue_key
