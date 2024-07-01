#!/bin/bash

#echo ""
#kubectl get namespace

# echo ""
# echo "-------[Node]-------"
# kubectl get node

echo ""
echo "-------[Pod]-------"
kubectl get pod

# echo ""
# echo "-------[Deployment]-------"
# kubectl get deploy

echo ""
echo "-------[Service]-------"
kubectl get service

echo ""
echo "-------[Ingress]-------"
kubectl get ingress

echo ""
echo "-------[HPA]-------"
kubectl get hpa

echo ""
#echo "-------[Configmap]-------"
#kubectl get configmap

#echo ""
#echo "-------[Secret]-------"
#kubectl get secret

