#!/bin/bash

#echo ""
#kubectl get namespace

echo ""
echo "-------[pod]-------"
kubectl get pod

echo ""
echo "-------[service]-------"
kubectl get service

echo ""
echo "-------[ingress]-------"
kubectl get ingress

echo ""
echo "-------[configmap]-------"
kubectl get configmap

echo ""
echo "-------[secret]-------"
kubectl get secret

