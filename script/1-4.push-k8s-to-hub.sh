#!/bin/bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
#set -e

docker login

docker push jnuho/fe-nginx-k8s
docker push jnuho/be-go-k8s
docker push jnuho/be-py
