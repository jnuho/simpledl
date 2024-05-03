#!/bin/bash

minikube kubectl -- delete -f ingress.yaml

minikube kubectl -- delete -f fe/nginx/service.yaml
minikube kubectl -- delete -f be/go/service.yaml
minikube kubectl -- delete -f be/py/service.yaml

minikube kubectl -- delete -f fe/nginx/deployment.yaml
minikube kubectl -- delete -f be/go/deployment.yaml
minikube kubectl -- delete -f be/py/deployment.yaml

#minikube kubectl -- delete secret regcred

minikube kubectl -- get pod
minikube kubectl -- get service
minikube kubectl -- get ingress

