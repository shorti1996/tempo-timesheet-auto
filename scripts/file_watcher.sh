#!/bin/sh

cd /shared || exit
# inotifywait requires package inotify-tools
inotifywait -m /shared/ -e create -e moved_to |
    while read -r dir action file; do
        echo "The file '$file' appeared in directory '$dir' via '$action'"
        # do something with the file
        extension="${file##*.}"
        if [ "$extension" = "tex" ]; then
            pdflatex -interaction=nonstopmode /shared/"${file}"
        fi
        if [ "${1:-0}" -eq 0 ]; then
            kill -SIGINT -$$
        fi
    done
