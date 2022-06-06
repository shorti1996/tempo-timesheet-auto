import json
import uuid
from pathlib import Path
from threading import Thread
from time import sleep
from uuid import UUID

import pyinotify
from flask import Flask, request, abort, send_file
from flask_cors import CORS

from config.consts import shared_path
from logic.app_logger import logger
from logic.flask_app.file_deleter import FileDeleter
from logic.flask_app.models import InvoiceCreationRequestDto
from logic.flask_app.routes import api_root_path, generate_invoice
from logic.universal_invoice.universal_invoice import InvoiceMaker


class InvoicerFlaskApp:
    PDF_PROCESSING_TIMEOUT_SECONDS = 10.0
    PDF_PROCESSING_SLEEP_STEP_SECONDS = 0.05

    def __init__(self):
        self.app: Flask = Flask(__name__)
        CORS(self.app)
        self.file_deleter = FileDeleter(shared_path)
        self.file_deleter.start()

        @self.app.route(str(api_root_path / generate_invoice), methods=['POST'])
        def invoice_generation():
            def inotify_callback(filename):
                def helper(event):
                    nonlocal ready
                    if filename and event.name == filename:
                        ready = True
                        return True

                return helper

            def watch():
                try:
                    notifier.loop()
                except (AttributeError, TypeError):
                    pass

            ready: bool = False
            invoice_id: UUID = uuid.uuid4()
            pdf_filename = f"{str(invoice_id)}.pdf"

            wm = pyinotify.WatchManager()
            notifier = pyinotify.Notifier(wm, inotify_callback, timeout=int(InvoicerFlaskApp.PDF_PROCESSING_TIMEOUT_SECONDS))
            mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE  # watched events
            wdd = wm.add_watch(str(shared_path), mask, rec=False, proc_fun=inotify_callback(pdf_filename))
            thr = Thread(target=watch).start()

            invoice_creation_request: InvoiceCreationRequestDto = InvoiceCreationRequestDto.from_dict(request.json)
            invoice_maker: InvoiceMaker = InvoiceMaker(invoice_creation_request.invoice_template_filename)
            tex_string: str = invoice_maker.render_template_latex(invoice_creation_request.invoice_data)
            InvoiceMaker.output_tex_string_to_file(tex_string, shared_path / Path(f"{str(invoice_id)}.tex"))
            logger.log(f"Waiting for {pdf_filename}")

            while not ready:
                sleep(InvoicerFlaskApp.PDF_PROCESSING_SLEEP_STEP_SECONDS)

            notifier.stop()
            try:
                return send_file(path_or_file=shared_path / pdf_filename, as_attachment=True)
            except FileNotFoundError:
                abort(404)
            return abort(500)

    def start(self):
        self.app.run(host='0.0.0.0', port=8282, debug=False)
        # self.app.run(host='0.0.0.0', port=8282, debug=True, use_reloader=False)


def response_200_ok():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
