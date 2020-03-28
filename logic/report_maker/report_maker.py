import os

from config.consts import pivot_table_hours_header, pivot_table_tasks_header, pivot_table_projects_header, order_number_template
from config.report_data import contractor, nip, initials, net_amount_due
from logic.report_maker.latexer import Latexer
from logic.report_maker.report_data_supplier import ReportDataSupplier

os.environ['OPENBLAS_NUM_THREADS'] = '1'
import pandas as pd

from logic.atlassian.issuer import Issuer
from logic.calendarer import get_current_day_string, str_to_date, get_months_last_day, date_to_str, get_months_first_day, get_months_number
from logic.worklogs.worklog_checker import AllWorklogChecker


class ReportMaker:
    def __init__(self, latexer=Latexer()):
        self.latexer = latexer

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
        df = df.rename(columns={'timeSpentSeconds': pivot_table_hours_header,
                                'projectName': pivot_table_projects_header,
                                'summary': pivot_table_tasks_header})

        pivot_table_latex_str = pd.pivot_table(df, values=pivot_table_hours_header, index=[pivot_table_projects_header, pivot_table_tasks_header],
                                               aggfunc=sum, margins=True, margins_name=pivot_table_hours_header).to_latex()

        supplier = ReportDataSupplier(date_to_str(get_months_first_day(str_to_date(day_anchor))),
                                      date_to_str(get_months_last_day(str_to_date(day_anchor))),
                                      nip,
                                      contractor,
                                      order_number_template % (get_months_number(str_to_date(day_anchor)), initials),
                                      list(set(df[pivot_table_projects_header])),
                                      net_amount_due,
                                      pivot_table_latex_str)
        self.render_report_latex(supplier)

    def render_report_latex(self, report_data_supplier: ReportDataSupplier):
        return self.latexer.render(**report_data_supplier.supply())


ReportMaker().make_report_month()
