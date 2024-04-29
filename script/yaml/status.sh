#!/bin/bash

echo ""

kubectl get namespace

echo ""

kubectl get pod -n simple
kubectl get service -n simple
kubectl get ingress -n simple

echo ""

kubectl get secret -n simple

