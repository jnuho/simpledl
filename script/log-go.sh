#!/bin/bash

# Get the name of the be-go pod
POD_NAME=$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep be-go-deployment)

# Log the output of the be-go pod with the --tail option
minikube kubectl -- logs --tail=10 $POD_NAME -f
