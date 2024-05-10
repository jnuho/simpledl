#!/bin/bash

set -e


#replace="s/microk8s kubectl/minikube kubectl --/g"
replace="s/minikube kubectl --/microk8s kubectl/g"

find . -type f \( -name '*.sh' -o -name '*.yaml' \) \
    -not -path "./replace.sh" \
    -print0 | xargs -0 sed -i "$replace"
