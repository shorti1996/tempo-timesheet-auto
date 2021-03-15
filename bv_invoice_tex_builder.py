import argparse

from config.consts import tex_files_output_path, root_path
from logic.bv_invoice.invoice_maker import InvoiceMaker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create tex file')
    parser.add_argument('-i', '--input-file', type=str, nargs=1, default=["bv_invoice"],
                        help='Input file name')
    parser.add_argument('-o', '--output-file', type=str, nargs=1, default=[tex_files_output_path / "bv_invoice.tex"],
                        help='Output file')

    args = parser.parse_args()
    invoice_maker = InvoiceMaker(args.input_file[0])
    data = invoice_maker.prepare_data_for_invoice()
    tex_string = invoice_maker.render_template_latex(data)
    invoice_maker.output_tex_string_to_file(tex_string, args.output_file[0])
