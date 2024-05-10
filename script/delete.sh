#!/bin/bash

microk8s kubectl delete -f ingress.yaml

microk8s kubectl delete -f service.yaml
microk8s kubectl delete -f be/go/service.yaml
microk8s kubectl delete -f be/py/service.yaml

microk8s kubectl delete -f deployment.yaml
microk8s kubectl delete -f be/go/deployment.yaml
microk8s kubectl delete -f be/py/deployment.yaml

#microk8s kubectl delete secret regcred

microk8s kubectl get pod
microk8s kubectl get service
microk8s kubectl get ingress

