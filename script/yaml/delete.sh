#!/bin/bash

kubectl delete -f ingress.yaml

kubectl delete -f fe/nginx/service.yaml
kubectl delete -f be/go/service.yaml
kubectl delete -f be/py/service.yaml

kubectl delete -f fe/nginx/deployment.yaml
kubectl delete -f be/go/deployment.yaml
kubectl delete -f be/py/deployment.yaml


kubectl get pod -n simple
kubectl get service -n simple
kubectl get ingress -n simple

