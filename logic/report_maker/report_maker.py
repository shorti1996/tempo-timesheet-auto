from typing import Any, Callable

import pandas as pd

from logic.atlassian.issuer import Issuer
from logic.calendarer import get_current_day_string, str_to_date, get_months_last_day, date_to_str
from logic.worklogs.worklog_checker import AllWorklogChecker


def let(x: Any, block: Callable[[Any], Any]):
    return block(x)


def apply(x, block, *args, **kwargs):
    block(x, *args, **kwargs)
    return x


def accumulate_hours(worklog):
    ...


class ReportMaker:
    def make_report_month(self, day_anchor: str = get_current_day_string()):
        month_start = str_to_date(day_anchor).replace(day=1)
        month_end = month_start.replace(day=get_months_last_day(month_start).day)
        worklogs = AllWorklogChecker().get_worklogs(day_from=date_to_str(month_start), day_to=date_to_str(month_end))
        issue_keys = list(set([worklog['issue']['key'] for worklog in worklogs]))
        issues = [Issuer().get_issue(key) for key in issue_keys]

        accumulated_data = {k: {} for k in issue_keys}
        for k, v in accumulated_data.items():
            issue = next(filter(lambda x: x['key'] == k, issues))
            accumulated_data[k]['summary'] = issue['fields']['summary']
            accumulated_data[k]['projectName'] = issue['fields']['project']['name']
            accumulated_data[k]['timeSpentSeconds'] = sum([w['timeSpentSeconds'] for w in worklogs if w['issue']['key'] == k])

        df = pd.DataFrame(accumulated_data).transpose()
        df['timeSpentSeconds'] = df['timeSpentSeconds'] / (60 * 60)
        df = df.rename(columns={'timeSpentSeconds': 'timeSpentHours'})

        pivot_table = pd.pivot_table(df, values='timeSpentHours', index=['projectName', 'summary'], aggfunc=sum)

        x = 0


ReportMaker().make_report_month()
