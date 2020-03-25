import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

from logic.worklogs.worklog_checker import ScrumWorklogChecker
from logic.worklogs.worklog_creator import ScrumWorklogCreator
from logic.worklogs.worklog_manager import ScrumWorklogManager
from model.worklog import WorklogPost


def prepare_worklog_manager():
    with open(Path(__file__).parent / 'response.json', 'r') as file:
        response_str = file.read()
    worklog_checker = ScrumWorklogChecker()
    worklog_checker.get_worklogs = lambda: json.loads(response_str)["results"]
    worklog_manager = ScrumWorklogManager(worklog_checker, ScrumWorklogCreator())
    ScrumWorklogManager.post_issues = lambda self, issues: None
    return worklog_manager


worklog_manager = prepare_worklog_manager()


class WorklogManagerTest(unittest.TestCase):
    def test_single_day_2020_03_25(self):
        with unittest.mock.patch.object(worklog_manager, 'post_issues',
                                        wraps=worklog_manager.post_issues) as monkey:
            worklog_manager.fill_missing_scrum_for_day(datetime(2020, 3, 25))
            monkey.assert_called_once_with([WorklogPost.create_with_defaults('2020-03-25')])

    def test_single_day_2020_03_26_already_filled(self):
        with unittest.mock.patch.object(worklog_manager, 'post_issues',
                                        wraps=worklog_manager.post_issues) as monkey:
            worklog_manager.fill_missing_scrum_for_day(datetime(2020, 3, 26))
            monkey.assert_called_once_with([])

    def test_week_2020_03_25(self):
        with unittest.mock.patch.object(worklog_manager, 'post_issues',
                                        wraps=worklog_manager.post_issues) as monkey:
            worklog_manager.fill_missing_scrum_for_week(datetime(2020, 3, 25))
            monkey.assert_called_once_with([WorklogPost.create_with_defaults('2020-03-23'),
                                            WorklogPost.create_with_defaults('2020-03-25'),
                                            WorklogPost.create_with_defaults('2020-03-27')])

    def test_week_until_2020_03_25(self):
        with unittest.mock.patch.object(worklog_manager, 'post_issues',
                                        wraps=worklog_manager.post_issues) as monkey:
            worklog_manager.fill_missing_scrum_for_week_until_day(datetime(2020, 3, 25))
            monkey.assert_called_once_with([WorklogPost.create_with_defaults('2020-03-23'),
                                            WorklogPost.create_with_defaults('2020-03-25')])
