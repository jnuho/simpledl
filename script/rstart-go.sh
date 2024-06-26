#!/bin/bash

# Get the name of the fe-nginx pod
kubectl delete -f be/go/deployment.yaml

sleep 2

kubectl apply -f be/go/deployment.yaml
