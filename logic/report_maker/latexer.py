import os
import subprocess
from pathlib import Path

import jinja2

from config.consts import default_report_output_path
from config.secrets import pdflatex_install_location


class Latexer:
    def __init__(self, templates_dir: os.path, template_file: str):
        self.latex_jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(templates_dir)
        )
        self.template = self.latex_jinja_env.get_template(template_file)

    def render_template(self, **kwargs):
        return self.template.render(**kwargs)

    @staticmethod
    def create_pdf(tex_string, output_dir=default_report_output_path, output_filename="output"):
        p = subprocess.run([pdflatex_install_location, '-jobname', output_filename, '-output-directory', output_dir],
                           stdout=subprocess.PIPE, input=tex_string, encoding='utf-8')
        print(p.stdout)
        return Path(output_dir) / (output_filename + '.pdf')
