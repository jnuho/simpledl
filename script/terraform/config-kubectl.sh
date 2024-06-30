#!/bin/bash

aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster

sleep 1

kubectl get svc -w
