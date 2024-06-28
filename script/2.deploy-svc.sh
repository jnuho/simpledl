#!/bin/bash

# fe-nginx
minikube kubectl -- apply -f deployment.yaml

# be-go
minikube kubectl -- apply -f service.yaml
minikube kubectl -- apply -f be/go/deployment.yaml
minikube kubectl -- apply -f be/go/service.yaml

# be-py
minikube kubectl -- apply -f be/py/deployment.yaml
minikube kubectl -- apply -f be/py/service.yaml

# mongodb, mongo-express
# minikube kubectl -- apply -f mongo/mongo-configmap.yaml
# minikube kubectl -- apply -f mongo/mongo-secret.yaml
# minikube kubectl -- apply -f mongo/mongodb.yaml
# minikube kubectl -- apply -f mongo/mongo-express.yaml
