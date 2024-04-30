#!/bin/bash

docker build -f ../../../dockerfiles/Dockerfile-nginx -t jnuho/fe-nginx ../../..
docker push jnuho/fe-nginx
