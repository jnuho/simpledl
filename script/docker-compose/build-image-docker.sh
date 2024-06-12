#!/bin/bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
#set -e

docker rmi jnuho/fe-nginx
docker rmi jnuho/be-go
docker rmi jnuho/be-py

docker build -f ../dockerfiles/Dockerfile-nginx -t jnuho/fe-nginx-docker ..
docker build -f ../dockerfiles/Dockerfile-go -t jnuho/be-go-docker ..
docker build -f ../dockerfiles/Dockerfile-py -t jnuho/be-py ..
