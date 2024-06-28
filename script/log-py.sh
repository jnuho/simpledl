#!/bin/bash

# Get the name of the be-py pod
POD_NAME=$(minikube kubectl -- get pods --no-headers -o custom-columns=":metadata.name" | grep be-py-deployment)

# Log the output of the be-py pod with the --tail option
minikube kubectl -- logs --tail=10 $POD_NAME -f
