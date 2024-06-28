#!/bin/bash

kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80
