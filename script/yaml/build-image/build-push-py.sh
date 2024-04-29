#!/bin/bash

docker build -f ../../../dockerfiles/Dockerfile-py -t jnuho/be-py ../../..
docker push jnuho/be-py
