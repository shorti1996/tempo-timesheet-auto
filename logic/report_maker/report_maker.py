import os

from config.consts import pivot_table_hours_header, pivot_table_tasks_header, pivot_table_projects_header, order_number_template
from config.consts import pivot_table_total_name
from config.secrets import tempo_auth_token, atlassian_login, atlassian_auth_token
from logic.report_maker.latexer import Latexer
from logic.report_maker.report_data_supplier import ReportDataSupplier

os.environ['OPENBLAS_NUM_THREADS'] = '1'
import pandas as pd

from logic.atlassian.issuer import Issuer
from logic.calendarer import get_current_day_string, str_to_date, get_months_last_day, date_to_str, get_months_number, get_months_first_day
from logic.worklogs.worklog_checker import AllWorklogChecker


class ReportMaker:
    def __init__(self, tempo_api_key, jira_login, jira_api_key,
                 period_from, period_to, contractor, initials, nip, net_amount_due, latexer=Latexer()):
        self.period_from = period_from
        self.period_to = period_to
        self.contractor = contractor
        self.initials = initials
        self.nip = nip
        self.net_amount_due = net_amount_due
        self.latexer = latexer
        self.worklog_checker = AllWorklogChecker(tempo_api_key)
        self.worklog_checker = AllWorklogChecker(tempo_api_key)
        self.issuer = Issuer(jira_login, jira_api_key)

    def make_report_month(self, day_anchor: str = get_current_day_string()):
        month_start = get_months_first_day(str_to_date(day_anchor))
        month_end = get_months_last_day(str_to_date(day_anchor))
        report_tex_string = self.make_report_tex_string(month_start, month_end)
        pdf_path = Latexer.create_pdf(report_tex_string)
        return pdf_path

    def make_report_tex_string(self, period_start, period_end):
        worklogs = self.worklog_checker.get_worklogs(day_from=date_to_str(period_start), day_to=date_to_str(period_end))
        issue_keys = list(set([worklog['issue']['key'] for worklog in worklogs]))
        issues = [self.issuer.get_issue(key) for key in issue_keys]
        accumulated_data = self.accumulate_data_for_pivot_table(issue_keys, issues, worklogs)
        df, pivot_table_latex_str = self.make_pivot_table(accumulated_data)
        supplier = ReportDataSupplier(date_to_str(period_start),
                                      date_to_str(period_end),
                                      self.nip,
                                      self.contractor,
                                      order_number_template % (get_months_number(period_start), self.initials),
                                      list(set(df[pivot_table_projects_header])),
                                      self.net_amount_due,
                                      pivot_table_latex_str)
        return self.render_report_latex(supplier)

    def accumulate_data_for_pivot_table(self, issue_keys, issues, worklogs):
        accumulated_data = {k: {} for k in issue_keys}
        for k, v in accumulated_data.items():
            issue = next(filter(lambda x: x['key'] == k, issues))
            accumulated_data[k]['summary'] = issue['fields']['summary']
            accumulated_data[k]['projectName'] = issue['fields']['project']['name']
            accumulated_data[k]['timeSpentSeconds'] = sum([w['timeSpentSeconds'] for w in worklogs if w['issue']['key'] == k])
        return accumulated_data

    def make_pivot_table(self, accumulated_data):
        df = pd.DataFrame(accumulated_data).transpose()
        df['timeSpentSeconds'] = df['timeSpentSeconds'] / (60 * 60)
        df = df.rename(columns={'timeSpentSeconds': pivot_table_hours_header,
                                'projectName': pivot_table_projects_header,
                                'summary': pivot_table_tasks_header})
        pivot_table_latex_str = pd.pivot_table(df, values=pivot_table_hours_header, index=[pivot_table_projects_header, pivot_table_tasks_header],
                                               aggfunc=sum, margins=True, margins_name=pivot_table_total_name).to_latex()
        return df, pivot_table_latex_str

    def render_report_latex(self, report_data_supplier: ReportDataSupplier):
        return self.latexer.render_template(**report_data_supplier.supply())


report_path = ReportMaker(tempo_api_key=tempo_auth_token,
                          jira_login=atlassian_login,
                          jira_api_key=atlassian_auth_token,
                          period_from='2020-03-02',
                          period_to='2020-03-31',
                          nip='1233212132',
                          contractor='Jan kowalski',
                          initials='WL',
                          net_amount_due='100').make_report_month()
x = 0
