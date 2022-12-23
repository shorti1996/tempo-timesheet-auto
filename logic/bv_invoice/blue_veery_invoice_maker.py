from datetime import date

from dateutil.relativedelta import relativedelta
from num2words import num2words

from config.consts import month_only_date_format, default_date_format, tex_files_output_path, template_files_path
from logic.bv_invoice.invoice_data_supplier import InvoiceDataYmlSupplier, load_invoice_yml, InvoiceDataCompleteSupplier
from logic.calendarer import str_to_date, get_months_first_day, get_months_last_day
from logic.universal_invoice.universal_invoice import InvoiceMaker


class BlueVeeryInvoiceMaker(InvoiceMaker):
    price_format = "{:,.2f}"
    decimals_only_format = "{:.2f}"
    month_year_format = '%m/%Y'

    def __init__(self, file_name: str = 'bv_invoice'):
        super().__init__(file_name)

    def prepare_data_for_invoice(self) -> InvoiceDataCompleteSupplier:
        invoice_yml: InvoiceDataYmlSupplier = load_invoice_yml(template_files_path / f"{self.file_name}.yml")
        invoice_data: InvoiceDataCompleteSupplier = InvoiceDataCompleteSupplier.from_dict(invoice_yml.to_dict())

        gross_amount = float(invoice_data.net_price)
        net_price = float(invoice_data.net_price)
        if invoice_data.invoice_date is None and invoice_data.invoice_month is not None:
            months_first_day = get_months_first_day(str_to_date(invoice_data.invoice_month, month_only_date_format))
            months_last_day = get_months_last_day(months_first_day)
            invoice_date = months_last_day
        elif invoice_data.invoice_date is not None and invoice_data.invoice_month is None:
            months_first_day = get_months_first_day(str_to_date(str(invoice_data.invoice_date), default_date_format))
            months_last_day = get_months_last_day(months_first_day)
            invoice_date = str_to_date(str(invoice_data.invoice_date), default_date_format)
        else:
            raise RuntimeError("invoiceDate or invoiceMonth is mandatory")
        payment_due = invoice_date + relativedelta(days=13)

        invoice_data.vat_price = format_price(0.0)
        invoice_data.vat_amount = format_price(0.0)
        invoice_data.net_price = format_price(net_price)
        invoice_data.net_amount = format_price(net_price)
        invoice_data.gross_amount = format_price(gross_amount)
        invoice_data.gross_amount_words_en = num2words(int(gross_amount))
        invoice_data.gross_amount_words_pl = num2words(int(gross_amount), lang='pl')
        invoice_data.gross_amount_hundredths = get_round_decimal_places(float(gross_amount))
        invoice_data.invoice_date = date.strftime(invoice_date, default_date_format)
        invoice_data.payment_due = date.strftime(payment_due, default_date_format)
        invoice_data.invoice_number = f"{invoice_yml.invoice_number}/{date.strftime(months_first_day, BlueVeeryInvoiceMaker.month_year_format)}"
        invoice_data.transaction_date = date.strftime(months_last_day, default_date_format)
        invoice_data.description = f"{invoice_yml.description} \\\\ {date.strftime(months_first_day, BlueVeeryInvoiceMaker.month_year_format)}"
        return invoice_data


def get_round_decimal_places(number: float, decimal_places=2):
    return "{:.2f}".format(round(number, decimal_places)).split('.')[1]


def format_price(number: float):
    return BlueVeeryInvoiceMaker.price_format.format(number).replace(',', ' ').replace('.', ',')


if __name__ == '__main__':
    invoice_maker = BlueVeeryInvoiceMaker()
    data = invoice_maker.prepare_data_for_invoice()
    tex_string = invoice_maker.render_template_latex(data)
    InvoiceMaker.output_tex_string_to_file(tex_string, tex_files_output_path / "test.tex")

    # report_path = InvoiceMaker().make_report_tex_string(invoice_data)
    x = 0
