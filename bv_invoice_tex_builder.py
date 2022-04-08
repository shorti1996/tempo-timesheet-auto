import argparse

from config.consts import tex_files_output_path
from logic.bv_invoice.blue_veery_invoice_maker import BlueVeeryInvoiceMaker
from logic.flask_app.flask_app import InvoicerFlaskApp
from logic.universal_invoice.universal_invoice import InvoiceMaker

# import pydevd_pycharm
# pydevd_pycharm.settrace('host.docker.internal', port=9191, stdoutToServer=True, stderrToServer=True, suspend=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create tex file')
    parser.add_argument('-i', '--input-file', type=str, nargs=1, default=["bv_invoice"],
                        help='Input file name')
    parser.add_argument('-o', '--output-file', type=str, nargs=1, default=[tex_files_output_path / "bv_invoice.tex"],
                        help='Output file')
    parser.add_argument('-s', '--server', action='store_true',
                        help='Start REST API server and wait for API calls. Ignore `-i` and `-o` options.')

    args = parser.parse_args()
    if args.server:
        InvoicerFlaskApp().start()
    else:
        invoice_maker = BlueVeeryInvoiceMaker(args.input_file[0])
        data = invoice_maker.prepare_data_for_invoice()
        tex_string = invoice_maker.render_template_latex(data)
        InvoiceMaker.output_tex_string_to_file(tex_string, args.output_file[0])
