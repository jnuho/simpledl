#!/bin/bash

docker build -f ../../../dockerfiles/Dockerfile-go -t jnuho/be-go ../../..
docker push jnuho/be-go
