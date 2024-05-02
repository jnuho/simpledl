#!/bin/bash

#!/bin/bash

# Get the current configmap and save it to a file
kubectl get configmap kube-proxy -n kube-system -o yaml > kube-proxy-configmap.yaml

# Use sed to replace the mode and strictARP values
sed -i 's/mode: ""/mode: "ipvs"/g' kube-proxy-configmap.yaml
sed -i 's/strictARP: false/strictARP: true/g' kube-proxy-configmap.yaml

# Apply the changes to the configmap
kubectl apply -f kube-proxy-configmap.yaml

# Clean up the temporary file
rm kube-proxy-configmap.yaml



kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-frr.yaml


cat <<EOF >> configmap.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: nat
  namespace: metallb-system
spec:
  addresses:
  - 192.168.49.100-192.168.49.110
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: empty
  namespace: metallb-system
EOF

kubectl apply -f configmap.yaml

kubectl rollout restart deployment controller -n metallb-system
