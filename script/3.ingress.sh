#!/bin/bash

# Enable nginx ingress controller
# 1. minikube addon
minikube addons enable ingress
# OR
# 2.helm
# helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
# helm install ingress-nginx ingress-nginx/ingress-nginx


sleep 2

# Define ingress routing rule
kubectl apply -f ingress.yaml
