from dataclasses import dataclass
from typing import Optional

import yaml
from dataclasses_json import dataclass_json, LetterCase

from logic.template_data_supplier import TemplateDataSupplier


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class InvoiceDataYmlSupplier(TemplateDataSupplier):
    supplier_data_line1: str
    supplier_data_line2: str
    supplier_data_line3: str
    client_data_line1: str
    client_data_line2: str
    client_data_line3: str
    supplier_vat_code: str
    client_vat_code: str
    description: str
    net_price: str
    invoice_month: str
    bank_account_number: str
    bic_swift_code: str
    invoice_number: Optional[str] = None


def load_invoice_yml(file: str) -> InvoiceDataYmlSupplier:
    with open(file, 'r') as stream:
        try:
            return InvoiceDataYmlSupplier.from_dict(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class InvoiceDataCompleteSupplier(InvoiceDataYmlSupplier):
    transaction_date: Optional[str] = None
    vat_price: Optional[str] = None
    vat_amount: Optional[str] = None
    net_amount: Optional[str] = None
    gross_amount: Optional[str] = None
    gross_amount_words_en: Optional[str] = None
    gross_amount_words_pl: Optional[str] = None
    gross_amount_hundredths: Optional[str] = None
    invoice_date: Optional[str] = None
    payment_due: Optional[str] = None
