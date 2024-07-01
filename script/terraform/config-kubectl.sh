#!/bin/bash

aws eks update-kubeconfig --region ap-northeast-2 --name my-cluster --profile terraform

sleep 1

kubectl get svc -w
