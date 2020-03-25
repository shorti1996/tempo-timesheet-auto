import json
from abc import abstractmethod

import tempo_requests
from config.consts import default_scrum_issue_key, default_workweek_days
from config.settings import api_url_worklogs
from logic.calendarer import get_current_day, get_week_days_str, date_to_str


class WorklogChecker:
    @property
    @abstractmethod
    def filter_predicate(self):
        pass

    def get_worklogs(self):
        response = tempo_requests.get(api_url_worklogs)
        results = json.loads(response.content)["results"]
        return results


class ScrumWorklogChecker(WorklogChecker):
    @property
    def filter_predicate(self):
        return lambda result: result['issue']['key'] == default_scrum_issue_key

    def get_scrum_issues(self):
        return filter(self.filter_predicate, self.get_worklogs())

    def get_worklogs_for_multiple_days(self,
                                       anchor_time=get_current_day(), days_num=default_workweek_days, days_str=None):
        if days_str is None:
            days_str = get_week_days_str(anchor_time, days_num)
        scrum_issues = self.get_scrum_issues()
        these_days_issues = [x for x in scrum_issues if x['startDate'] in days_str]
        return these_days_issues

    def get_worklogs_for_day(self, anchor_time=get_current_day()):
        scrum_issues = self.get_scrum_issues()
        that_day_issue = next(iter([x for x in scrum_issues if x['startDate'] == date_to_str(anchor_time)]), None)
        return that_day_issue
