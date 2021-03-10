from datetime import date

from num2words import num2words

from config.consts import month_only_date_format, default_date_format, root_path
from config.settings import template_files_path
from logic.bv_invoice.invoice_data_supplier import InvoiceDataYmlSupplier, load_invoice_yml, InvoiceDataCompleteSupplier
from logic.calendarer import str_to_date, get_months_first_day
from logic.report_maker.latexer import Latexer


class InvoiceMaker:
    price_format = "{:,.2f}"
    decimals_only_format = "{:.2f}"

    def __init__(self, file_name: str = 'bv_invoice'):
        self.file_name = file_name
        self.latexer = Latexer(templates_dir=template_files_path, template_file=f"{self.file_name}.tex")

    def prepare_data_for_invoice(self) -> InvoiceDataCompleteSupplier:
        invoice_yml: InvoiceDataYmlSupplier = load_invoice_yml(template_files_path / f"{self.file_name}.yml")
        invoice_data = InvoiceDataCompleteSupplier.from_dict(invoice_yml.to_dict())

        gross_amount = float(invoice_data.net_price)
        net_price = float(invoice_data.net_price)

        invoice_data.vat_price = format_price(0.0)
        invoice_data.net_price = format_price(net_price)
        invoice_data.gross_amount = format_price(gross_amount)
        invoice_data.gross_amount_words_en = num2words(int(gross_amount))
        invoice_data.gross_amount_words_pl = num2words(int(gross_amount), lang='pl')
        invoice_data.gross_amount_hundredths = get_round_decimal_places(float(gross_amount))
        months_first_day = get_months_first_day(str_to_date(invoice_data.invoice_month, month_only_date_format))
        invoice_data.invoice_date = date.strftime(months_first_day, default_date_format)
        payment_due = str_to_date(f"{invoice_data.invoice_month}-14")
        invoice_data.payment_due = date.strftime(payment_due, default_date_format)
        invoice_data.invoice_number = f"001/{date.strftime(months_first_day, '%m/%Y')}"
        return invoice_data

    def render_template_latex(self, invoice_data_supplier: InvoiceDataYmlSupplier):
        return self.latexer.render_template(**invoice_data_supplier.supply())

    def create_pdf(self, report_tex_string: str):
        pdf_path = self.latexer.create_pdf(report_tex_string, root_path)
        return pdf_path


def get_round_decimal_places(number: float, decimal_places=2):
    return "{:.2f}".format(round(number, decimal_places)).split('.')[1]


def format_price(number: float):
    return InvoiceMaker.price_format.format(number).replace(',', ' ').replace('.', ', ')


invoice_maker = InvoiceMaker()
data = invoice_maker.prepare_data_for_invoice()
tex_string = invoice_maker.render_template_latex(data)
pdf_path = invoice_maker.create_pdf(tex_string)

# report_path = InvoiceMaker().make_report_tex_string(invoice_data)
x = 0
