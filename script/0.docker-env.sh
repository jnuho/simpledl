#!/bin/bash

# To switch back to your default Docker daemon after using Minikube's,
# you just need to unset the environment variables
# that were set by the eval $(minikube docker-env) command.
# You can do this by closing your current terminal and opening a new one.
# The environment variables set by the eval command are only valid in the current shell,
# so they won't affect new shells.
# If you want to unset them without closing your terminal, you can use the following commands:

#unset DOCKER_TLS_VERIFY
#unset DOCKER_HOST
#unset DOCKER_CERT_PATH
#unset MINIKUBE_ACTIVE_DOCKERD
set -e
if [ -z "$1" ]
  then
  echo "argument {bash|cmd|powershell} is required for --shell"
  exit 1
fi

SHELL=$1
PROFILE_NAME=$(minikube profile list | awk '/\*/ {print $2}')
eval $(minikube -p ${PROFILE_NAME} docker-env --shell=${SHELL})
