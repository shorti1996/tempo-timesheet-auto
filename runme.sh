#!/bin/bash

docker build -f Dockerfile -t shorti1996/latexer:latest .
docker run -it --rm --entrypoint='' -v "`pwd`"/pdf:/pdf shorti1996/latexer:latest  cp test.pdf /pdf/test.pdf
