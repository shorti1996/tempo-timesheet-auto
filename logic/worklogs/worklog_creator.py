from logic.calendarer import get_current_day
from model.worklog import WorklogPost


class ScrumWorklogCreator:
    @staticmethod
    def create_worklog_for_day(anchor_time=get_current_day()):
        issue = WorklogPost.create_with_defaults(anchor_time)
        return issue
