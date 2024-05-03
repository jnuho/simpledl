#!/bin/bash

minikube kubectl -- apply -f deployment.yaml
minikube kubectl -- apply -f be/go/deployment.yaml
minikube kubectl -- apply -f be/py/deployment.yaml

minikube kubectl -- apply -f service.yaml
minikube kubectl -- apply -f be/go/service.yaml
minikube kubectl -- apply -f be/py/service.yaml

