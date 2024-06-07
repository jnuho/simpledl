#!/bin/bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
#set -e

docker login

docker push jnuho/fe-nginx-docker
docker push jnuho/be-go-docker
docker push jnuho/be-py
