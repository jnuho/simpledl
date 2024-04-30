#!/bin/bash

kubectl apply -f fe/nginx/deployment.yaml
kubectl apply -f be/go/deployment.yaml
kubectl apply -f be/py/deployment.yaml

kubectl apply -f fe/nginx/service.yaml
kubectl apply -f be/go/service.yaml
kubectl apply -f be/py/service.yaml

kubectl apply -f ingress.yaml

