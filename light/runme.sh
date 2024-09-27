#! /bin/bash

cd dockerfiles || exit
docker login docker-repository.bv-soft.pl
docker-compose up
