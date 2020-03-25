import datetime
from datetime import timedelta
from time import strptime

from config.consts import default_date_format, default_workweek_days


def get_current_day():
    return datetime.date.today()


def date_to_str(time, fmt=default_date_format):
    def format_time(fmt, time):
        return time.strftime(fmt)

    if isinstance(time, list):
        return [format_time(fmt, x) for x in time]
    elif isinstance(time, datetime.date):
        return format_time(fmt, time)
    else:
        return None


def str_to_date(time_str, fmt=default_date_format):
    return datetime.datetime.strptime(time_str, fmt)


def get_current_day_string(fmt=default_date_format):
    today = datetime.date.today()
    return date_to_str(today, fmt)


def get_week_start(time=get_current_day()):
    return time - timedelta(days=time.weekday())


def get_week_days(time=get_current_day(), num_days=default_workweek_days):
    return [get_week_start(time) + datetime.timedelta(days=x) for x in
            range(num_days)]  # - 1)]  # -1 because the start day counts as well


def get_week_days_str(time=get_current_day(), num_days=default_workweek_days):
    return date_to_str(get_week_days(time, num_days))


def get_workweek_days(time=get_current_day(), days_in_workweek=default_workweek_days):
    return get_week_days(time, days_in_workweek)


def get_workweek_days_str(time=get_current_day(), days_in_workweek=default_workweek_days):
    return date_to_str(get_week_days(time, days_in_workweek))


def is_day_workday(time=get_current_day(), days_in_workweek=default_workweek_days):
    return date_to_str(time) in date_to_str(get_workweek_days(time, days_in_workweek))
