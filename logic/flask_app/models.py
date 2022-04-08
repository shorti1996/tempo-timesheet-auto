from dataclasses import dataclass
from typing import Dict, Optional

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class InvoiceCreationRequestDto:
    invoice_template_filename: str
    invoice_data: Optional[Dict[str, str]] = None

