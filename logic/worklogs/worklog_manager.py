import tempo_requests
from config.consts import default_workweek_days
from config.settings import api_url_worklogs
from logic.calendarer import get_current_day, str_to_date, get_workweek_days_str
from logic.worklogs.worklog_checker import ScrumWorklogChecker
from logic.worklogs.worklog_creator import ScrumWorklogCreator


class ScrumWorklogManager:
    def __init__(self):
        self.worklog_checker = ScrumWorklogChecker()
        self.worklog_creator = ScrumWorklogCreator()

    def fill_missing_scrum_for_day(self, time_anchor=get_current_day()):
        that_day_scrum = self.worklog_checker.get_worklogs_for_day(time_anchor)
        if that_day_scrum is None:
            issue = self.worklog_creator.create_worklog_for_day(time_anchor)
            self.post_issues(issue)

    def fill_missing_scrum_for_week(self, time_anchor=get_current_day(), days_num=default_workweek_days):
        that_week_scrum = self.worklog_checker.get_worklogs_for_week(time_anchor, days_num)
        week_days_str = get_workweek_days_str(time_anchor, days_num)
        missing_days = [day for day in week_days_str if day not in [issue['startDate'] for issue in that_week_scrum]]
        missing_issues = [self.worklog_creator.create_worklog_for_day(str_to_date(day)) for day in missing_days]
        ScrumWorklogManager.post_issues(missing_issues)

    def fill_missing_scrum_for_week_until_day(self, time_anchor=get_current_day(), days_num=default_workweek_days):
        that_week_scrum = self.worklog_checker.get_worklogs_for_week(time_anchor, days_num)
        week_days_str = get_workweek_days_str(time_anchor, days_num)
        missing_days = [day for day in week_days_str if day not in [issue['startDate'] for issue in that_week_scrum]]
        missing_issues = [self.worklog_creator.create_worklog_for_day(str_to_date(day)) for day in missing_days]
        ScrumWorklogManager.post_issues(missing_issues)

    @staticmethod
    def post_issues(issues):
        def post_issue(issue):
            tempo_requests.post(api_url_worklogs, json=issue.create_dict())

        if isinstance(issues, list):
            [post_issue(issue) for issue in issues]
        else:
            post_issue(issues)
