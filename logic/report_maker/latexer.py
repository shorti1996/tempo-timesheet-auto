import jinja2
import os


class Latexer:
    latex_jinja_env = jinja2.Environment(
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
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )

    def __init__(self, template_file='resources/bsg_po_template.tex'):
        self.template = Latexer.latex_jinja_env.get_template(template_file)

    def render(self, **kwargs):
        print(self.template.render(**kwargs))
