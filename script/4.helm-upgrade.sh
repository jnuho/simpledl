#!/bin/bash

if [ "$(kubectl config current-context)" = "minikube" ]; then
    helm upgrade tst-release ./tst-chart -f ./tst-chart/values.dev.yaml
else
    aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster --profile terraform
    helm upgrade tst-release ./tst-chart -f ./tst-chart/values.prd.yaml
fi
