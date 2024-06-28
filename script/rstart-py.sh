#!/bin/bash

# Get the name of the fe-nginx pod
minikube kubectl -- delete -f be/py/deployment.yaml

sleep 2

minikube kubectl -- apply -f be/py/deployment.yaml
minikube kubectl -- get pod --watch
