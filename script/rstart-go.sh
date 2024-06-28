#!/bin/bash

# Get the name of the fe-nginx pod
minikube kubectl -- delete -f be/go/deployment.yaml

sleep 2

minikube kubectl -- apply -f be/go/deployment.yaml
minikube kubectl -- get pod --watch
