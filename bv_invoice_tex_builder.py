from config.consts import tex_files_output_path
from logic.bv_invoice.invoice_maker import InvoiceMaker

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Create tex file')
    # parser.add_argument('-i', '--input-file', type=str, nargs=1, default=[root_path / "resources" / "bv_invoice.tex"],
    #                     help='Output file')
    # parser.add_argument('-i', '--data-file', type=str, nargs=1, default=[root_path / "resources" / "bv_invoice.yml"],
    #                     help='Output file')
    # parser.add_argument('-o', '--output-file', type=str, nargs=1, default=[tex_files_output_path / "test.tex"],
    #                     help='Output file')

    # args = parser.parse_args()
    invoice_maker = InvoiceMaker()
    data = invoice_maker.prepare_data_for_invoice()
    tex_string = invoice_maker.render_template_latex(data)
    invoice_maker.output_tex_string_to_file(tex_string, tex_files_output_path / "test.tex")
