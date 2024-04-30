#!/bin/bash

kubectl delete -f ingress.yaml

kubectl delete -f fe/nginx/service.yaml
kubectl delete -f be/go/service.yaml
kubectl delete -f be/py/service.yaml

kubectl delete -f fe/nginx/deployment.yaml
kubectl delete -f be/go/deployment.yaml
kubectl delete -f be/py/deployment.yaml


kubectl get pod
kubectl get service
kubectl get ingress

