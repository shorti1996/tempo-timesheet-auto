import unittest
from pathlib import Path

from logic.scheduler.scheduler import Scheduler
from model.worklog import WorklogPost

scheduler = Scheduler()
scheduler.load_schedule_from_file(str(Path(__file__).parent / "test_schedule.json"))


def create_cd_72(day):
    return WorklogPost('CD-72', 27000, day, '00:00:00', 'DEV-14998 Investigate handling request for customer type', '5e5cbdc996f7d50ca054fc2a')


class WorklogManagerTest(unittest.TestCase):
    def test_2020_03_25_no_default_daily_but_already_present(self):
        the_day = "2020-03-25"
        issues = scheduler.get_issues_for_day(the_day)
        self.assertEqual([WorklogPost.create_with_defaults(the_day),
                          create_cd_72(the_day)],
                         issues)

    def test_2020_03_26_default_daily_without_flag_in_json(self):
        the_day = "2020-03-26"
        issues = scheduler.get_issues_for_day(the_day)
        self.assertEqual([create_cd_72(the_day),
                          WorklogPost.create_with_defaults(the_day)],
                         issues)

    def test_2020_03_27_empty_workday_should_append_daily(self):
        the_day = "2020-03-27"
        issues = scheduler.get_issues_for_day(the_day)
        self.assertEqual([WorklogPost.create_with_defaults(the_day)],
                         issues)

    def test_2020_03_28_scheduled_saturday_should_append_daily(self):
        the_day = "2020-03-28"
        issues = scheduler.get_issues_for_day(the_day)
        self.assertEqual([create_cd_72(the_day),
                          WorklogPost.create_with_defaults(the_day)],
                         issues)

    def test_2020_03_29_empty_sunday_should_be_empty(self):
        the_day = "2020-03-29"
        issues = scheduler.get_issues_for_day(the_day)
        self.assertEqual([],
                         issues)
