#!/bin/bash

# SA for load balancer controller
kubectl apply -f 10-lb-controller-sa.yaml

# install
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=testcluster-001 \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller

kubectl get deploy -n kube-system aws-load-balancer-controller


