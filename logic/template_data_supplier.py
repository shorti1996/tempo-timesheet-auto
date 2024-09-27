from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TemplateDataSupplier:
    def supply(self):
        return self.to_dict()
