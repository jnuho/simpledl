#!/bin/bash

kubectl delete -f ingress.yaml

kubectl delete -f service.yaml
kubectl delete -f be/go/service.yaml
kubectl delete -f be/py/service.yaml

kubectl delete -f deployment.yaml
kubectl delete -f be/go/deployment.yaml
kubectl delete -f be/py/deployment.yaml

# mongodb, mongo-express
#kubectl delete -f mongo/mongo-configmap.yaml
#kubectl delete -f mongo/mongo-secret.yaml
#kubectl delete -f mongo/mongodb.yaml
#kubectl delete -f mongo/mongo-express.yaml

#kubectl delete secret regcred

kubectl get pod
kubectl get service
kubectl get ingress

