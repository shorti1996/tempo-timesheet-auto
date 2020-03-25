import argparse

from logic.calendarer import get_current_day_string, str_to_date
from logic.worklogs.worklog_manager import ScrumWorklogManager

parser = argparse.ArgumentParser(description='Fill tempo with daily. Daily.')
parser.add_argument('--day', type=str, nargs=1, default=get_current_day_string(),
                    help='an anchor date (default: today), YYYY-MM-DD')
parser.add_argument('--action', choices=['day', 'week', 'week-until-today'], default='day',
                    help='choose which action you want to perform (default: fill for today)')

args = parser.parse_args()
worklog_manager = ScrumWorklogManager()
day = str_to_date(args.day)
if args.action == 'day':
    worklog_manager.fill_missing_scrum_for_day(day)
elif args.action == 'week':
    worklog_manager.fill_missing_scrum_for_week(day)
elif args.action == 'week-until-today':
    worklog_manager.fill_missing_scrum_for_week_until_day(day)
