#!/bin/bash

# fe-nginx
microk8s kubectl apply -f deployment.yaml

# be-go
microk8s kubectl apply -f service.yaml
microk8s kubectl apply -f be/go/deployment.yaml
microk8s kubectl apply -f be/go/service.yaml

# be-py
microk8s kubectl apply -f be/py/deployment.yaml
microk8s kubectl apply -f be/py/service.yaml

# mongodb, mongo-express
microk8s kubectl apply -f mongo/mongo-configmap.yaml
microk8s kubectl apply -f mongo/mongo-secret.yaml
microk8s kubectl apply -f mongo/mongodb.yaml
microk8s kubectl apply -f mongo/mongo-express.yaml
