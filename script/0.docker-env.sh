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
# check shell type for corresponding operating systems
# in order to use it as a command argument
if [ -n "$BASH_VERSION" ]; then
  SHELL_TYPE="bash"
elif [ -n "$COMSPEC" ] && [ -z "$BASH_VERSION" ]; then
  SHELL_TYPE="cmd"
elif [ -n "$PSVersionTable" ]; then
  SHELL_TYPE="powershell"
else
  echo "unknown"
  exit 1
fi

PROFILE_NAME=$(minikube profile list | awk '/\*/ {print $2}')

# configure your local Docker client to use the Docker daemon inside the Minikube instance.
# This allows your local Docker client and the Docker client inside Minikube
# to share the same Docker daemon, so images built by one client can be run by the other.
eval $(minikube -p ${PROFILE_NAME} docker-env --shell=${SHELL_TYPE})

echo "Configured to use the Docker daemon inside the Minikube instance!"

