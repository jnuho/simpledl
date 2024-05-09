#!/bin/bash

microk8s kubectl -- apply -f deployment.yaml
microk8s kubectl -- apply -f be/go/deployment.yaml
microk8s kubectl -- apply -f be/py/deployment.yaml

microk8s kubectl -- apply -f service.yaml
microk8s kubectl -- apply -f be/go/service.yaml
microk8s kubectl -- apply -f be/py/service.yaml

