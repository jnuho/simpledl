#!/bin/bash

# Get the name of the fe-nginx pod
kubectl delete -f deployment.yaml

sleep 2

kubectl apply -f deployment.yaml
