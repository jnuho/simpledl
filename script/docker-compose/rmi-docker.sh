#!/bin/bash

docker rmi script-fe-nginx
docker rmi script-be-go
docker rmi script-be-py

docker images -a
docker ps -a
