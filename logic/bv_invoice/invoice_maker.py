from datetime import date
from pathlib import Path

from dateutil.relativedelta import relativedelta
from num2words import num2words

from config.consts import month_only_date_format, default_date_format, root_path, tex_files_output_path, template_files_path
from logic.bv_invoice.invoice_data_supplier import InvoiceDataYmlSupplier, load_invoice_yml, InvoiceDataCompleteSupplier
from logic.calendarer import str_to_date, get_months_first_day, get_months_last_day
from logic.report_maker.latexer import Latexer


class InvoiceMaker:
    price_format = "{:,.2f}"
    decimals_only_format = "{:.2f}"
    month_year_format = '%m/%Y'

    def __init__(self, file_name: str = 'bv_invoice'):
        self.file_name = file_name
        self.latexer = Latexer(templates_dir=template_files_path, template_file=f"{self.file_name}.tex")

    def prepare_data_for_invoice(self) -> InvoiceDataCompleteSupplier:
        invoice_yml: InvoiceDataYmlSupplier = load_invoice_yml(template_files_path / f"{self.file_name}.yml")
        invoice_data: InvoiceDataCompleteSupplier = InvoiceDataCompleteSupplier.from_dict(invoice_yml.to_dict())

        gross_amount = float(invoice_data.net_price)
        net_price = float(invoice_data.net_price)
        months_first_day = get_months_first_day(str_to_date(invoice_data.invoice_month, month_only_date_format))
        months_last_day = get_months_last_day(months_first_day)
        payment_due = months_first_day + relativedelta(days=13, months=1)

        invoice_data.vat_price = format_price(0.0)
        invoice_data.vat_amount = format_price(0.0)
        invoice_data.net_price = format_price(net_price)
        invoice_data.net_amount = format_price(net_price)
        invoice_data.gross_amount = format_price(gross_amount)
        invoice_data.gross_amount_words_en = num2words(int(gross_amount))
        invoice_data.gross_amount_words_pl = num2words(int(gross_amount), lang='pl')
        invoice_data.gross_amount_hundredths = get_round_decimal_places(float(gross_amount))
        invoice_data.invoice_date = date.strftime(months_last_day, default_date_format)
        invoice_data.payment_due = date.strftime(payment_due, default_date_format)
        invoice_data.invoice_number = f"{invoice_yml.invoice_number}/{date.strftime(months_first_day, InvoiceMaker.month_year_format)}"
        invoice_data.transaction_date = date.strftime(months_last_day, default_date_format)
        invoice_data.description = f"{invoice_yml.description} \\\\ {date.strftime(months_first_day, InvoiceMaker.month_year_format)}"
        return invoice_data

    def render_template_latex(self, invoice_data_supplier: InvoiceDataYmlSupplier):
        return self.latexer.render_template(**invoice_data_supplier.supply())

    def output_tex_string_to_file(self, tex_string: str, output_path: Path):
        with open(output_path, 'w') as file:
            file.write(tex_string)

    def create_pdf(self, tex_string: str):
        pdf_path = self.latexer.create_pdf(tex_string, root_path)
        return pdf_path


def get_round_decimal_places(number: float, decimal_places=2):
    return "{:.2f}".format(round(number, decimal_places)).split('.')[1]


def format_price(number: float):
    return InvoiceMaker.price_format.format(number).replace(',', ' ').replace('.', ',')


if __name__ == '__main__':
    invoice_maker = InvoiceMaker()
    data = invoice_maker.prepare_data_for_invoice()
    tex_string = invoice_maker.render_template_latex(data)
    invoice_maker.output_tex_string_to_file(tex_string, tex_files_output_path / "test.tex")

    # report_path = InvoiceMaker().make_report_tex_string(invoice_data)
    x = 0
