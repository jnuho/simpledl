#!/bin/bash

kubectl create namespace <namespace>


curl -sL https://istio.io/downloadIstioctl | ISTIO_VERSION=1.18.1 TARGET_ARCH=x86_64 sh -
cd ~/.istioctl/bin/
cp istioctl ~/000.eks/004.istio


kubectl label namespace <namespace> istio-injection=enabled

