FROM pandoc/latex:latest as latexer
RUN tlmgr update --self
RUN tlmgr install titlesec adjustbox collectbox makecell multirow
RUN apk add inotify-tools
WORKDIR /app
COPY ./scripts/file_watcher.sh .
# EMPTY VARIABLE
ENV SERVER ${1:+1}
ENTRYPOINT /app/file_watcher.sh $SERVER
