#!/bin/bash

#echo ""
#minikube kubectl -- get namespace

echo ""
echo "-------[pod]-------"
minikube kubectl -- get pod

echo ""
echo "-------[deployment]-------"
minikube kubectl -- get deploy

echo ""
echo "-------[service]-------"
minikube kubectl -- get service

echo ""
echo "-------[ingress]-------"
minikube kubectl -- get ingress

echo ""
echo "-------[configmap]-------"
minikube kubectl -- get configmap

echo ""
echo "-------[secret]-------"
minikube kubectl -- get secret

