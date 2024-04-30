#!/bin/bash

source ../../.env

kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=$DOCKERHUB_NAME \
  --docker-password=$DOCKERHUB_PW \
  --docker-email=$DOCKERHUB_EMAIL

kubectl apply -f fe/nginx/deployment.yaml
kubectl apply -f be/go/deployment.yaml
kubectl apply -f be/py/deployment.yaml

kubectl apply -f fe/nginx/service.yaml
kubectl apply -f be/go/service.yaml
kubectl apply -f be/py/service.yaml

kubectl apply -f ingress.yaml

