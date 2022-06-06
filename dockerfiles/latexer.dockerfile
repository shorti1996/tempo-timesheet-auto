FROM pandoc/latex:latest as latexer
RUN tlmgr update --self
RUN tlmgr install titlesec adjustbox collectbox makecell multirow
RUN apk add inotify-tools
WORKDIR /app
COPY ./scripts/file_watcher.sh .
# EMPTY VARIABLE
ARG SERVER
ENTRYPOINT /app/file_watcher.sh $SERVER
