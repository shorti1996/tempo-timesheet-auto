import argparse

from logic.calendarer import get_current_day_string, str_to_date
from logic.scheduler.scheduler import Scheduler
from logic.worklogs.worklog_manager import ScrumWorklogManager, WorklogManager

parser = argparse.ArgumentParser(description='Fill tempo with daily. Daily.')
parser.add_argument('-d', '--day', type=str, nargs=1, default=[get_current_day_string()],
                    help='an anchor date (default: today), YYYY-MM-DD')
parser.add_argument('-l', '--list', action='store_const', const=True,
                    help='if used, no worklogs will be created on the server, this just lists worklogs that would be created')
parser.add_argument('-s', '--scheduler', action='store_const', const=True,
                    help='if used, the script will be in a scheduler mode, which means it reads schedule.json for a specified day and reports issues '
                         'from that schedule instead of just reporting the daily for that day')
parser.add_argument('--scheduler-message', type=str, nargs=1, default=['Hello, below is your schedule for today!'],
                    help='if in scheduler mode, this message will be printed')
parser.add_argument('-a', '--action', choices=['day', 'week', 'week-until-today'], default='day',
                    help='choose which action you want to perform (default: fill for today)')

args = parser.parse_args()
scheduler_mode = bool(args.scheduler)
day = str_to_date(args.day[0])

if scheduler_mode:
    if len(args.scheduler_message[0]) > 0:
        print(args.scheduler_message[0])
    scheduler = Scheduler()
    scheduler.load_schedule_from_file()
    issues_for_day = scheduler.get_issues_for_day(args.day[0])
    WorklogManager(list_only=bool(args.list)).post_issues(issues_for_day)
else:
    worklog_manager = ScrumWorklogManager(list_only=bool(args.list))
    if args.action == 'day':
        worklog_manager.fill_missing_scrum_for_day(day)
    elif args.action == 'week':
        worklog_manager.fill_missing_scrum_for_week(day)
    elif args.action == 'week-until-today':
        worklog_manager.fill_missing_scrum_for_week_until_day(day)
