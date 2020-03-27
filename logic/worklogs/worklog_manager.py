from api_web import tempo_requests
from config.consts import tempo_api_url_worklogs, default_workweek_days
from logic.calendarer import get_current_day, str_to_date, get_workweek_days_str, days_difference_from_week_start, \
    date_to_str, is_day_workday
from logic.worklogs.worklog_checker import ScrumWorklogChecker
from logic.worklogs.worklog_creator import ScrumWorklogCreator


class WorklogManager:
    def __init__(self, list_only=False, print_on_post=True):
        self.list_only = list_only
        self.print_on_post = print_on_post

    def post_issues(self, issues):
        def post_issue(issue):
            if self.print_on_post:
                print("post:\n" + str(issue.create_dict()))
            tempo_requests.post(tempo_api_url_worklogs, json=issue.create_dict())

        if not self.list_only:
            if isinstance(issues, list):
                [post_issue(issue) for issue in issues]
            else:
                post_issue(issues)
            if self.print_on_post:
                print("post_issues: OK")
        else:
            print("Skipped post_issues for:\n" + "\n".join([str(issue.create_dict()) for issue in issues]))


class ScrumWorklogManager(WorklogManager):
    def __init__(self, worklog_checker=ScrumWorklogChecker(), worklog_creator=ScrumWorklogCreator(), list_only=False):
        super().__init__(list_only)
        self.worklog_checker = worklog_checker
        self.worklog_creator = worklog_creator
        self.list_only = list_only

    def fill_missing_scrum_for_given_days(self, days_str):
        issues_for_these_days = self.worklog_checker.get_worklogs_for_multiple_days(days_str=days_str)
        missing_days = [day for day in days_str if day not in [issue['startDate'] for issue in issues_for_these_days]]
        print("MISSING SCRUM:\n" + str(missing_days))
        missing_issues = [self.worklog_creator.create_worklog_for_day(str_to_date(day)) for day in missing_days]
        self.post_issues(missing_issues)

    def fill_missing_scrum_for_day(self, time_anchor=get_current_day()):
        if is_day_workday(time_anchor):
            self.fill_missing_scrum_for_given_days([date_to_str(time_anchor)])

    def fill_missing_scrum_for_week(self, time_anchor=get_current_day(), days_num=default_workweek_days):
        self.fill_missing_scrum_for_given_days(get_workweek_days_str(time_anchor, days_num))

    def fill_missing_scrum_for_week_until_day(self, time_anchor=get_current_day()):
        days_delta = days_difference_from_week_start(time_anchor) + 1
        self.fill_missing_scrum_for_given_days(get_workweek_days_str(time_anchor, days_delta))
