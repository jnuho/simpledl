#!/bin/bash

# fe-nginx
kubectl apply -f deployment.yaml

# be-go
kubectl apply -f service.yaml
kubectl apply -f be/go/deployment.yaml
kubectl apply -f be/go/service.yaml

# be-py
kubectl apply -f be/py/deployment.yaml
kubectl apply -f be/py/service.yaml

# mongodb, mongo-express
# kubectl apply -f mongo/mongo-configmap.yaml
# kubectl apply -f mongo/mongo-secret.yaml
# kubectl apply -f mongo/mongodb.yaml
# kubectl apply -f mongo/mongo-express.yaml
