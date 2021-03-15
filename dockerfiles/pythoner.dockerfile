FROM python:3.8-buster as pythoner
WORKDIR /app
# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD rm -r /shared/*; python bv_invoice_tex_builder.py -i ${FILENAME} -o /shared/${FILENAME}.tex