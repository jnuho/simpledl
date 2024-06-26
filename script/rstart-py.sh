#!/bin/bash

# Get the name of the fe-nginx pod
kubectl delete -f be/py/deployment.yaml

sleep 2

kubectl apply -f be/py/deployment.yaml
