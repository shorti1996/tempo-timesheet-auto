FROM pandoc/latex:latest as latexer
RUN tlmgr update --self
RUN tlmgr install titlesec adjustbox collectbox makecell multirow

FROM python:3.8-buster as pythoner
WORKDIR /app
# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#VOLUME ./output ./output
RUN python bv_invoice_tex_builder.py
RUN cat output/test.tex

FROM latexer as latexer2
WORKDIR /app
VOLUME ./pdf /pdf
COPY --from=pythoner /app/output/test.tex .
RUN pdflatex test.tex
RUN cp test.pdf /pdf/
CMD echo okk
