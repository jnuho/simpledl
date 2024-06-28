#!/bin/bash

#echo ""
#minikube kubectl -- get namespace

# echo ""
# echo "-------[Node]-------"
# minikube kubectl -- get node

echo ""
echo "-------[Pod]-------"
minikube kubectl -- get pod

# echo ""
# echo "-------[Deployment]-------"
# minikube kubectl -- get deploy

echo ""
echo "-------[Service]-------"
minikube kubectl -- get service

echo ""
echo "-------[Ingress]-------"
minikube kubectl -- get ingress

echo ""
#echo "-------[Configmap]-------"
#minikube kubectl -- get configmap

#echo ""
#echo "-------[Secret]-------"
#minikube kubectl -- get secret

