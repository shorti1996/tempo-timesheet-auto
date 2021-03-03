from dataclasses import dataclass

import yaml
from dataclasses_json import dataclass_json, LetterCase

from logic.template_data_supplier import TemplateDataSupplier


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class InvoiceDataSupplier(TemplateDataSupplier):
    invoice_number: str
    supplier_data_line1: str
    supplier_data_line2: str
    supplier_data_line3: str
    client_data_line1: str
    client_data_line2: str
    client_data_line3: str
    supplier_vat_code: str
    client_vat_code: str
    description: str

    @staticmethod
    def load(file: str):
        with open(file, 'r') as stream:
            try:
                return InvoiceDataSupplier.from_dict(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)
