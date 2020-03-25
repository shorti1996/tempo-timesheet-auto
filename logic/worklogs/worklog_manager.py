import tempo_requests
from config.consts import default_workweek_days
from config.settings import api_url_worklogs
from logic.calendarer import get_current_day, str_to_date, get_workweek_days_str, days_difference_from_week_start, date_to_str
from logic.worklogs.worklog_checker import ScrumWorklogChecker
from logic.worklogs.worklog_creator import ScrumWorklogCreator


class ScrumWorklogManager:
    def __init__(self, worklog_checker=ScrumWorklogChecker(), worklog_creator=ScrumWorklogCreator()):
        self.worklog_checker = worklog_checker
        self.worklog_creator = worklog_creator

    def fill_missing_scrum_for_given_days(self, days_str):
        issues_for_these_days = self.worklog_checker.get_worklogs_for_multiple_days(days_str=days_str)
        missing_days = [day for day in days_str if day not in [issue['startDate'] for issue in issues_for_these_days]]
        print("MISSING:\n" + str(missing_days))
        missing_issues = [self.worklog_creator.create_worklog_for_day(str_to_date(day)) for day in missing_days]
        ScrumWorklogManager.post_issues(missing_issues)

    def fill_missing_scrum_for_day(self, time_anchor=get_current_day()):
        self.fill_missing_scrum_for_given_days([date_to_str(time_anchor)])

    def fill_missing_scrum_for_week(self, time_anchor=get_current_day(), days_num=default_workweek_days):
        self.fill_missing_scrum_for_given_days(get_workweek_days_str(time_anchor, days_num))

    def fill_missing_scrum_for_week_until_day(self, time_anchor=get_current_day()):
        days_delta = days_difference_from_week_start(time_anchor) + 1
        self.fill_missing_scrum_for_given_days(get_workweek_days_str(time_anchor, days_delta))

    @staticmethod
    def post_issues(issues):
        def post_issue(issue):
            tempo_requests.post(api_url_worklogs, json=issue.create_dict())

        if isinstance(issues, list):
            [post_issue(issue) for issue in issues]
        else:
            post_issue(issues)
        print("post_issues: OK")
