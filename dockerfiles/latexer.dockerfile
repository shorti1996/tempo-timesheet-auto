FROM pandoc/latex:latest as latexer
RUN tlmgr update --self
RUN tlmgr install titlesec adjustbox collectbox makecell multirow
ENTRYPOINT while [ ! -f /shared/${FILENAME}.tex ]; do echo "Waiting for .tex file to be generated"; sleep 1; done; pdflatex /shared/${FILENAME}.tex; cp ${FILENAME}.pdf /shared/
