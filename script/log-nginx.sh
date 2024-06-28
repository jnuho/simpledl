#!/bin/bash

# Get the name of the fe-nginx pod
POD_NAME=$(minikube kubectl -- get pods --no-headers -o custom-columns=":metadata.name" | grep fe-nginx-deployment)

# Log the output of the fe-nginx pod with the --tail option
minikube kubectl -- logs --tail=10 $POD_NAME -f
