#!/bin/bash

#echo ""
#microk8s kubectl get namespace

echo ""
echo "-------[Pod]-------"
microk8s kubectl get pod

echo ""
echo "-------[Deployment]-------"
microk8s kubectl get deploy

echo ""
echo "-------[Service]-------"
microk8s kubectl get service

echo ""
echo "-------[Ingress]-------"
microk8s kubectl get ingress

echo ""
echo "-------[Configmap]-------"
microk8s kubectl get configmap

echo ""
echo "-------[Secret]-------"
microk8s kubectl get secret

