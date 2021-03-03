from config.settings import template_files_path
from logic.bv_invoice.invoice_data_supplier import InvoiceDataSupplier
from logic.calendarer import get_current_day_string, str_to_date, get_months_last_day, get_months_first_day
from logic.report_maker.latexer import Latexer


class InvoiceMaker:
    def __init__(self, file_name: str = 'bv_invoice'):
        self.file_name = file_name
        self.latexer = Latexer(templates_dir=template_files_path, template_file=f"{self.file_name}.tex")

    def make_report_month(self, day_anchor: str = get_current_day_string()):
        month_start = get_months_first_day(str_to_date(day_anchor))
        month_end = get_months_last_day(str_to_date(day_anchor))
        report_tex_string = self.make_report_tex_string(month_start, month_end)
        pdf_path = self.latexer.create_pdf(report_tex_string)
        return pdf_path

    def make_report_tex_string(self):
        supplier = InvoiceDataSupplier.load(template_files_path / f"{self.file_name}.yml")
        return self.render_template_latex(supplier)

    def render_template_latex(self, invoice_data_supplier: InvoiceDataSupplier):
        return self.latexer.render_template(**invoice_data_supplier.supply())


report_path = InvoiceMaker().make_report_tex_string()
x = 0
