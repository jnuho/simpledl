#!/bin/bash

# Get the name of the fe-nginx pod
minikube kubectl -- delete -f deployment.yaml

sleep 2

minikube kubectl -- apply -f deployment.yaml
minikube kubectl -- get pod --watch
