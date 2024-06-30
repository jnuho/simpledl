#!/bin/bash

# Get the name of the fe-nginx pod
kubectl delete -f deployment.yaml
kubectl delete -f be/go/deployment.yaml
kubectl delete -f be/py/deployment.yaml

sleep 2

kubectl apply -f deployment.yaml
kubectl apply -f be/go/deployment.yaml
kubectl apply -f be/py/deployment.yaml
kubectl get pod --watch
