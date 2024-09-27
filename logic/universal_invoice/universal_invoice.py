from pathlib import Path
from typing import Union, Dict

from config.consts import root_path, template_files_path
from logic.flask_app.latex_escaper import tex_escape_recursive
from logic.report_maker.latexer import Latexer
from logic.template_data_supplier import TemplateDataSupplier


class InvoiceMaker:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.latexer: Latexer = Latexer(templates_dir=template_files_path, template_file=f"{self.file_name}.tex")

    def render_template_latex(self, invoice_data_supplier: Union[TemplateDataSupplier, Dict]):
        data_dict: Dict
        if isinstance(invoice_data_supplier, TemplateDataSupplier):
            data_dict = invoice_data_supplier.supply()
        else:
            data_dict = tex_escape_recursive(invoice_data_supplier)
        return self.latexer.render_template(**data_dict)

    @staticmethod
    def output_tex_string_to_file(tex_string: str, output_path: Path):
        with open(output_path, 'w') as file:
            file.write(tex_string)

    @staticmethod
    def create_pdf(tex_string: str):
        pdf_path = Latexer.create_pdf(tex_string, root_path)
        return pdf_path
