
### System overview

|<img src="https://i.imgur.com/w8PxxXk.png" alt="simpledl architecture" width="420">|
|:--:| 
| *kubernetes architecture of my application* |

<!-- more -->

[↑ Back to top](#)
<br><br>

* <i style="font-size:24px" class="fa">&#xf09b;</i> <a href="https://github.com/jnuho/simpledl" target="_blank">`github.com/jnuho/simpledl`</a>

- [System overview](#system-overview)
- [Binary classification](#binary-classification)
- [Virtualbox network architecture](#virtualbox-network-architecture)
- [Application demo](#application-demo)
- [Kubernetes setup](#kubernetes-setup)
- [Virtualbox setup](#virtualbox-setup)
- [Microservices](#microservices)
    - [CORS issue](#cors-issue)
    - [Backend - Golang web server](#backend-golang-web-server)
    - [Backend - Python web server](#backend-python-web-server)
        - [Mathematical background for deep learning image recognizer](#mathematical-background-for-deep-learning-image-recognizer)
        - [Image Classification](#image-classification)
        - [Pytorch](#pytorch)
    - [Frontend - local setup](#frontend-local-setup)
- [Dockerize for image build](#dockerize)
- [1. Minikube implementation](#minikube-implementation)
- [2. Microk8s implemntation](#microk8s-implemntation)
- [3. GCP implementation](#gcp-implementation)


### Binary classification

It is a basic deep learning image recognizers, one of which was covered in Andrew Ng's coursera course. I plan to test two simple deep learning models to identify cat images and hand-written digits (0-9), respectively and return the result of identification to the browser.

[↑ Back to top](#)
<br><br>


### Virtualbox network architecture

I had to construct a virtualbox environment in which my kubernetes cluster and application will be deployed. 🔥


|<img src="https://d17pwbfgewyq5y.cloudfront.net/virtualbox_NAT.drawio.png" alt="pods" width="520">|
|:--:| 
| *NAT network* |


[↑ Back to top](#)
<br><br>


### Application demo

The following image is the result of deployment on **multi-node Kuberentes cluster.**

| <img src="https://d17pwbfgewyq5y.cloudfront.net/microk8s-result.gif" alt="pods" width="680"> |
|:--:| 
| *web application* |

|<img src="https://d17pwbfgewyq5y.cloudfront.net/microk8s-pods.png" alt="pods" width="680"> |
|:--:| 
| *Kubernetes resources* |

[↑ Back to top](#)
<br><br>

### Kubernetes setup

- Kubernetes : 3-node cluster w/ [microk8s](https://microk8s.io/docs/getting-started).
- Docker and `docker-compose` for testing
- Microservices architecture
    - Frontend : Nginx (with html, css, js) as a reverse proxy server
    - Backend : Python uvicorn, Golang go-gin as backend web server
- Deep learning algorithm for binary classification using basic `numpy`
    - includes forward and [backward propagation](https://en.wikipedia.org/wiki/Backpropagation)
    - TODO: `pytorch` for cat/non-cat recognizer
- Virtualbox (cli) to create 3 master nodes (ubuntu) for k8s cluster

I recently focused on testing a 3-master-node [Kubernetes](https://kubernetes.io/) cluster setup using MicroK8s, with basic web service functionality. **My next goal** is to enhance the Python backend service by adding a fundamental deep learning algorithm. Specifically, the Python backend worker will perform binary classification on cat vs. non-cat images from a given image URL. For implementation, I initially explored using `numpy` for backward/forward propagation, and I am currently exploring the `PyTorch` library.


[↑ Back to top](#)
<br><br>


### Virtualbox Setup

- Download ubuntu iso image
- Run vm instacne using iso image
- Install ubuntu

- Hosts: 10.0.2.3, 10.0.2.4, 10.0.2.5
- OS: Ubuntu 24.04 server


```bat
vboxmanage list dhcpservers
vboxmanage list natnetworks
vboxmanage list vms

VBoxManage dhcpserver remove --netname k8snetwork
VBoxManage natnetwork remove --netname k8snetwork

VBoxManage unregistervm ubuntu-1 --delete
VBoxManage unregistervm ubuntu-2 --delete
VBoxManage unregistervm ubuntu-3 --delete

./vb-create.bat > log.txt 2>&1
```


```bat
VBoxManage natnetwork add --netname k8snetwork --network "10.0.2.0/24" --enable --dhcp on
VBoxManage dhcpserver add --netname k8snetwork --server-ip "10.0.2.2" --netmask "255.255.255.0" --lower-ip "10.0.2.3" --upper-ip "10.0.2.254" --enable

vboxmanage dhcpserver restart --network=k8snetwork

for /L %%i in (1, 1, 3) do (
    REM Create VM
    VBoxManage createvm --name ubuntu-%%i --register --ostype Ubuntu_64
    REM ...
    REM ...
)

REM Set up port forwarding rules
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Rule 1:tcp:[127.0.0.1]:22021:[10.0.2.3]:22"
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Rule 2:tcp:[127.0.0.1]:22022:[10.0.2.4]:22"
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Rule 3:tcp:[127.0.0.1]:22023:[10.0.2.5]:22"

REM application port
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Http:tcp:[127.0.0.1]:80:[10.0.2.3]:80"
```

```sh
# ethernet device info
nmcli d

nmcli d show enp0s3

ip a dev enp0s3

sudo ip link set enp0s3 down
sudo ip link set enp0s3 up
```


[↑ Back to top](#)
<br><br>

### Microservices

1. frontend: nginx (nodejs vite in local) + javascript + html + css
2. backend/web: golang (gin framework)
3. backend/worker: python (fast api, numpy, scikit-learn)
    - https://fastapi.tiangolo.com/tutorial/


### Communication between services

1. **HTTP/REST API**: You can expose a REST API on your Python backend and have the Golang server make HTTP requests to it. This is similar to how your JavaScript frontend communicates with the Golang server

2. **gRPC/Protobuf**: gRPC is a high-performance, open-source universal RPC framework, and Protobuf (short for Protocol Buffers) is a method for serializing structured data. You can use gRPC and Protobuf for communication between your Golang and Python applications. This method is efficient and type-safe, but it might be a bit more complex to set up compared to a REST API.

3. **Message Queue**: If your use case involves asynchronous processing or you want to decouple your Golang and Python applications, you can use a message queue like RabbitMQ or Apache Kafka. In this setup, your Golang application would publish messages to the queue, and your Python application would consume these messages.

4. **Socket Programming**: You can use sockets for communication if both your Golang and Python applications are running on the same network. This method requires a good understanding of network programming.

5. **Database**: If both applications have access to a shared database, you can use the database as a communication medium. One application writes to the database, and the other one reads from it.


[↑ Back to top](#)
<br><br>


### CORS issue

- https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

When a web application tries to make a request to a server that’s on a different domain, protocol, or port, it encounters a CORS (Cross-Origin Resource Sharing) issue. Add headers to backend server accordingly

```
For security reasons, browsers restrict cross-origin HTTP requests initiated from scripts.
For example, fetch() and XMLHttpRequest follow the same-origin policy.

This means that a web application using those APIs can only request resources
from the same origin the application was loaded from unless the response
from other origins includes the right CORS headers.

=> Add appropriate headers in golang server.
```


[↑ Back to top](#)
<br><br>

### Backend Golang web server

- `go.mod`, `go.sum` must be in github repo root directory

```sh
cd simpledl
go mod init github.com/jnuho/simpledl
go mod tidy


cd simpledl/pkg
go mod init github.com/jnuho/simpledl/pkg
go mod tidy


cd simpledl/cmd/backend-web-server
go mod init github.com/jnuho/simpledl/cmd/backend-web-server
go mod tidy
```


[↑ Back to top](#)
<br><br>


### Backend Python web server

- Use FastAPI + Unicorn
    - FastAPI is an ASGI (<b>Asynchronous</b> Server Gateway Interface) framework which requires an ASGI server to run.
    - Unicorn is a lightning-fast ASGI server implementation

- install python (download .exe from python.org)
    - check Add to PATH option (required)


- Run the python web server

```sh
uvicorn main:app --port 3002
```


[↑ Back to top](#)
<br><br>

#### Mathematical background for deep learning image recognizer

The basic operations for forward and backward propagations in deep learning algorithm are as follows:

- Forward propagation for layer $l$: $a^{[l-1]}\rightarrow a^{[l]}, z^{[l]}, w^{[l]}, b^{[l]}$

    $Z^{[l]} = W^{[l]} A^{[l-1]} + b^{[l]}$

    $A^{[l]} = g^{[l]} (Z^{[l]})$

    (for $i=1,\dots,L$ with initial value $A^{[0]} = X$)

<br>

- Backward propagation for layer $l$: $da^{[l]} \rightarrow da^{[l-1]},dW^{[l]}, db^{[l]}$

    $dZ^{[l]} = dA^{[l]} * {g^{[l]}}^{'}(Z^{[l]})$

    $dW^{[l]} = \frac{1}{m}dZ^{[l]}{A^{[l-1]}}^T$

    $db^{[l]} = \frac{1}{m}np.sum(dZ^{[l]}, axis=1, keepdims=True)$

    $dA^{[l-1]} = {W^{[l]}}^T dZ^{[l]} = \frac{dJ}{dA^{[l-1]}} = \frac{dZ^{[l]}}{dA^{[l-1]}} \frac{dJ}{dZ^{[l]}} = \frac{dZ^{[l]}}{dA^{[l-1]}} dZ^{[l]}$

    (with initial value $dZ^{[L]} = A^{[L]}-Y$)



[↑ Back to top](#)
<br><br>

### Image Classification

- cat vs.non-cat image classification and hand-written digits recognition
- https://www.youtube.com/watch?v=JgtWVML4Ykg&ab_channel=SheldonVon
- https://detexify.kirelabs.org/classify.html
- https://mco-mnist-draw-rwpxka3zaa-ue.a.run.app/



[↑ Back to top](#)
<br><br>

### Frontend - local setup

- Download    & install nodejs 20.12.2
    - for local development using `vite`

```sh
npm create vite@latest
    ? Project name: lesson11
    > choose Vanilla, TypeScript
```

- Edit `package.json` to edit port and dependencies

```json
    "scripts": {
        "dev": "vite --host 0.0.0.0 --port 8080",
        "build": "tsc && vite build",
        "preview": "vite preview"
    },

    "dependencies": {
        "axios": "^1.6.8"
    }
```

Note that I will be using nginx instead in production environment. I used nodejs vite just for local development environment.

```sh
# install dependencies specified in package.json
# install if package.json changes e.g. project name
npm i
npm run dev
    VITE v5.2.9    ready in 180 ms

    ➜    Local:     http://localhost:4200/
    ➜    Network: use --host to expose
    ➜    press h + enter to show help
```

- Edit code
    - Write `index.html`
    - Create directory: `./model`, `./templates`
    - Define models and templates
    - Edit `main.ts`



[↑ Back to top](#)
<br><br>

### Dockerize

**NOTE**: It is crucial to optimize Docker images to be as compact as possible.
One strategy to achieve this is by utilizing base images that are minimalistic, such as the Alpine image.

- [NOTE on defining backend endpoint in frontend](https://stackoverflow.com/a/56375180/23876187)
    - frontend app is not in any container, but the javascript is served from container as a js script file to <b>your browser</b>!

- frontend nginx service



[↑ Back to top](#)
<br><br>

### Minikube implementation

To set up your Nginx, Golang, and Python microservices on Minikube, you'll need to create Kubernetes Deployment and Service YAML files for each of your microservices. You'll also need to set up an Ingress controller to expose your services to the public. Here's a high-level overview of the steps:

1. **Install Minikube**: If you haven't already, you'll need to install Minikube on your machine. Minikube is a tool that lets you run Kubernetes locally.

- ubuntu 24.04 install minikube

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# unintstall
#sudo dpkg -r minikube
```


[↑ Back to top](#)
<br><br>

2. **Start Minikube**: Once installed, you can start a local Kubernetes cluster with the command `minikube start`.

```sh
# As a TROUBLE SHOOTING:
docker context use default
    default
    Current context is now "default"

minikube start
```


[↑ Back to top](#)
<br><br>

3. **Create secret**

3-1. Login to docker hub

```
docker login --username YOUR_USERNAME
```

3-2. Create secret

```
k create secret docker-registry regcred \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username=USER \
    --docker-password=PW \
    --docker-email=EMAIL

k get secret
```



[↑ Back to top](#)
<br><br>

4. **Create Deployment and Service YAML Files**: For each of your microservices (Nginx, Golang, Python), you'll need to create a Deployment and a Service. The Deployment defines your application and the Docker image it uses, while the Service defines how your application is exposed to the network

4-1. deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: fe-nginx-deployment
spec:
    replicas: 1
    # Deployement manages pods with label 'app: fe-nginx
    selector:
        matchLabels:
            app: fe-nginx
    # define labels for the Pods:
    #     must be matched by service.yaml > spec.selector
    template:
        metadata:
            labels:
                app: fe-nginx
        spec:
            containers:
            - name: fe-nginx
                image: jnuho/fe-nginx:latest
                ports:
                - containerPort: 80
            imagePullSecrets:
            - name: regcred

```


[↑ Back to top](#)
<br><br>

4-2. service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
    name: fe-nginx-service
    namespace: simple
spec:
    # must match deployment.yaml > spec.template.metadata.labels
    selector:
        app: fe-nginx
    ports:
        - protocol: TCP
            port: 8080
            targetPort: 80
    type: ClusterIP
```



[↑ Back to top](#)
<br><br>

5. **Apply the YAML Files**: Once you've created your YAML files, you can apply them to your Kubernetes cluster with the command `kubectl apply -f <filename.yaml>`.


[↑ Back to top](#)
<br><br>


6. **Enable Ingress Controller**:

6-1. NGINX ingress controller using Minikube addons: you can use the command `minikube addons enable ingress`

```sh
minikube addons enable ingress
```


[↑ Back to top](#)
<br><br>

6-2. Nginx ingress controller

- [setting up an NGINX ingress controller](https://medium.com/@amirhosseineidy/how-to-set-up-nginx-ingress-controller-in-local-server-6cc4bd7d6a6b) in a bare metal or local server:


Ingress is an API in Kubernetes that routes traffic to different services, making applications accessible to clients from the Kubernetes cluster. Among multiple choices like HAProxy or Envoy for setting up an ingress controller, NGINX is the most popular one. It is powered by the NGINX web server and is a fast and secure controller that delivers your applications to the clients easily.

- Install NGINX ingress controller with `helm`

```sh
# inside cmd or powershell
winget install Helm.Helm

# RESTART terminal and do:
helm upgrade --install ingress-nginx ingress-nginx \
    --repo https://kubernetes.github.io/ingress-nginx \
    --namespace ingress-nginx --create-namespace
```

- Check if ingress controller is working:

```sh
helm list
    NAME                        NAMESPACE             REVISION                UPDATED                                                                 STATUS                    CHART                                     APP VERSION
    ingress-nginx     default                 1                             2024-04-30 14:26:18.9350713 +0900 KST     deployed                ingress-nginx-4.10.1        1.10.1

k get ClusterRole | grep ingress
    ingress-nginx                                                                                                                    2024-04-30T07:01:05Z

k get all
    NAME                                                                                     READY     STATUS        RESTARTS     AGE
    pod/ingress-nginx-controller-cf668668c-zvkd9     1/1         Running     0                    44s

    NAME                                                                                 TYPE                     CLUSTER-IP             EXTERNAL-IP     PORT(S)                                            AGE
    service/ingress-nginx-controller                         LoadBalancer     10.100.168.236     <pending>         80:32020/TCP,443:31346/TCP     44s
    service/ingress-nginx-controller-admission     ClusterIP            10.107.208.79        <none>                443/TCP                                            44s
    service/kubernetes                                                     ClusterIP            10.96.0.1                <none>                443/TCP                                            4m8s

    NAME                                                                             READY     UP-TO-DATE     AVAILABLE     AGE
    deployment.apps/ingress-nginx-controller     1/1         1                        1                     44s

    NAME                                                                                                 DESIRED     CURRENT     READY     AGE
    replicaset.apps/ingress-nginx-controller-cf668668c     1                 1                 1             44s
```


[↑ Back to top](#)
<br><br>

7. **Create an Ingress YAML File**: The Ingress YAML file will define the rules for routing external traffic to your services. You'll need to specify the host and path for each service, and the service that should handle traffic to each host/path


[↑ Back to top](#)
<br><br>

8. **Apply the Ingress YAML File**: Just like with the Deployment and Service files, you can apply the Ingress file with `kubectl apply -f <ingress-filename.yaml>`.

- Ingress rules
    - Ingress rules are resources that help route services to your desired domain name or prefix. They are divided into prefix and DNS.
    - .yaml mainifest for ingress rules

```sh
k apply ingress.yaml
k get ingress
    NAME                             CLASS     HOSTS                                ADDRESS                PORTS     AGE
    fe-nginx-ingress     nginx     my-app.example.com     192.168.49.2     80            4m35s
```


[↑ Back to top](#)
<br><br>


9. **Access Your Services**: With the Ingress set up, you should be able to access your services from outside your Kubernetes cluster. You can get the IP address of your Minikube cluster with the command `minikube ip`, and then access your services at that IP


- Accessing application
    - For accessing these applications in a local cluster, you should access it through node port (30000 ports) or use a reverse proxy to send them.
    - But is there any way to access app on port 80 or 443?
        - use 1.`Port-forward` or 2.`MetalLB` to allow access to app on port 80 or 443.

### 9-1. Port Forward

```sh
k get svc -n ingress-nginx
    NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
    ingress-nginx-controller             NodePort    10.109.183.14    <none>        80:31078/TCP,443:31420/TCP   6m17s
    ingress-nginx-controller-admission   ClusterIP   10.110.101.115   <none>        443/TCP                      6m17s


# In Chrome browser, "http://localhost:8080" -> ingress controller on 80
k port-forward -n <namespace> svc/<service-name> <local-port>:<service-port>
# k port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80 3001:3001 3002:3002
k port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80
# k get svc -n ingress-nginx svc/ingress-nginx-controller -o yaml
#k edit svc -n ingress-nginx svc/ingress-nginx-controller
# spec:
#   ports:
#   - name: http
#     port: 80
#     protocol: TCP
#     targetPort: 80
#   - name: https
#     port: 443
#     protocol: TCP
#     targetPort: 443
#   - name: custom-port
#     port: 3001
#     protocol: TCP
#     targetPort: 3001

```

The need for port-forwarding arises due to the way Kubernetes networking and Minikube are structured. Here's a breakdown of why you might need to use port-forwarding and why direct access might not work without it:

### Why Direct Access Might Not Work

9-1-1. **Network Isolation:**
   - **Kubernetes Networking:** Kubernetes clusters are designed to have an isolated network. Services within the cluster communicate with each other via internal cluster IPs that are not accessible from the outside world directly.
   - **Minikube Networking:** Minikube sets up a local virtual machine (VM) on your computer. This VM has its own network namespace, separate from your host machine's network. The services running inside Minikube are isolated from your host machine by default.

9-1-2. **ClusterIP Services:**
   - **ClusterIP Type:** The services you've listed (`be-go-service`, `be-py-service`, `fe-nginx-service`, and `kubernetes`) are of type `ClusterIP`. This means they are only accessible within the cluster. External traffic from your host machine cannot reach these services directly.

9-1-3. **Minikube IP Address:**
   - Minikube typically runs on a virtual IP address, such as `192.168.49.2` in your case. Accessing this IP directly from your host might not be straightforward due to network isolation.

### Why Port-Forwarding is Needed

Port-forwarding provides a bridge between your host machine and the Kubernetes cluster, allowing you to access cluster services from your local machine as if they were running locally.

- **Accessing Cluster Services:**
   - Port-forwarding allows you to map a port on your local machine to a port on a pod or service within the cluster. This makes it possible to access cluster services using `localhost` on your host machine.

- **Bypassing Network Isolation:**
   - By forwarding a port, you bypass the network isolation of the cluster, making it possible to communicate with services running inside Minikube directly from your host.

### Alternative Approaches

If you prefer not to use port-forwarding, there are other approaches you can consider:

- **Minikube Tunnel:**
   - Minikube provides a `minikube tunnel` command that can create a network tunnel to your cluster, making services of type `LoadBalancer` accessible from your host machine.

   ```sh
   minikube tunnel
   ```

- **NodePort Services:**
   - Change the service type to `NodePort`, which exposes the service on a port on each node of the cluster. You can then access the service using the Minikube IP and the NodePort.

   Example of changing a service to NodePort:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: fe-nginx-service
   spec:
     type: NodePort
     ports:
       - port: 8080
         targetPort: 8080
         nodePort: 30080  # Example NodePort
     selector:
       app: fe-nginx
   ```

- **Ingress with Minikube IP:**
   - You can use the Minikube IP address and configure your `/etc/hosts` file to point `localhost` to the Minikube IP.

### Summary

Using `kubectl port-forward` is a convenient and straightforward way to access your services without altering service types or cluster configurations. It helps bridge the network isolation between your host machine and the Kubernetes cluster set up by Minikube.

[↑ Back to top](#)
<br><br>


### 9-2. Installing Metallb

```sh
# strictARP to true
kubectl edit configmap -n kube-system kube-proxy

    apiVersion: kubeproxy.config.k8s.io/v1alpha1
    kind: KubeProxyConfiguration
    mode: "ipvs"
    ipvs:
        strictARP: true

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-frr.yaml

kubectl get pods -n metallb-system
    NAME                                                    READY     STATUS        RESTARTS     AGE
    controller-596589985b-jrnmk     1/1         Running     0                    34m
    speaker-hdrmc                                 4/4         Running     0                    34m
```

- Now set a range IPs for your local load balancer by creating a configMap. 
    - Remember that the set of IP addresses you apply must be in the same range as your nodes IPs

The range of IP addresses you choose for MetalLB should be in the same subnet as your nodes' IPs. These IP addresses are used by MetalLB to assign to services of type LoadBalancer.
Using command, `k get node -o wide`, the INTERNAL-IP of my node is 192.168.49.2. So, choose a range of IP addresses in the 192.168.49.x range for MetalLB. For example, 192.168.49.100-192.168.49.110 as my range.

The IP addresses you choose for MetalLB should be reserved for MetalLB's use and should not conflict with any other devices on your network.

```yaml
# to see ip range for node
kubectl get nodes -o wide
    NAME             STATUS     ROLES                     AGE     VERSION     INTERNAL-IP        EXTERNAL-IP     OS-IMAGE                         KERNEL-VERSION                                             CONTAINER-RUNTIME
    minikube     Ready        control-plane     41m     v1.30.0     192.168.49.2     <none>                Ubuntu 22.04.4 LTS     5.15.146.1-microsoft-standard-WSL2     docker://26.0.1

cat > configmap.yaml
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


k apply -f configmap.yaml

kubectl rollout restart deployment controller -n metallb-system

# check EXTERNAL-IP for nginx-controller is assigned!!!
# the external IPS is assigned to your NGINX load balancer service and all other load balancer typed services.
k get svc
    NAME                                                                 TYPE                     CLUSTER-IP             EXTERNAL-IP            PORT(S)                                            AGE
    ingress-nginx-controller                         LoadBalancer     10.100.168.236     192.168.49.100     80:32020/TCP,443:31346/TCP     68m
```


[↑ Back to top](#)
<br><br>

- DNS Setup
    - Finally, you need to set the domain names defined in the ingress rules in your DNS server or hosts file
    - edit hosts file, `C:\Windows\System32\drivers\etc\hosts`

```
192.168.49.100 my-app.example.com
```


[↑ Back to top](#)
<br><br>

### 10. Tailscale

- [`Tailscale Funnel Example`](https://tailscale.com/kb/1247/funnel-examples)
- [`Tailscale Funnel Minikube Guide`](https://tailscale.com/learn/managing-access-to-kubernetes-with-tailscale)
- With `Tailscale Funnel`, you can expose local services, individual folders, or even plain text to the public internet over HTTPS.


- Create Tailscale account and Download
    - Now talescale dashboard shows your Machines (ip)

- Create Minikube local cluster on your Device (Windows in my case)

- Deploy Tailscale in Your Kubernetes Cluster
    - Create auth key in Tailscale dashboard: `Settings > Keys > Generate auth key`
    - Copy the key

- Copy the following YAML manifest and save it to `tailscale-secret.yaml` in your working directory:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tailscale-auth
stringData:
  TS_AUTHKEY: tskey-0123456789abcdef
```

- Next, you must create a Kubernetes service account, role, and role binding to configure role-based access control (RBAC) for your Tailscale deployment. You'll run your Tailscale pods as this new service account. The pods will be able to use the granted RBAC permissions to perform limited interactions with your Kubernetes cluster.

Copy the following YAML manifest to `tailscale-rbac.yaml`:


```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tailscale

---

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tailscale
rules:
  - apiGroups: [""]
    resourceNames: ["tailscale-auth"]
    resources: ["secrets"]
    verbs: ["get", "update", "patch"]

---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: tailscale
subjects:
  - kind: ServiceAccount
    name: tailscale
roleRef:
  kind: Role
  name: tailscale
  apiGroup: rbac.authorization.k8s.io
```

- For each sidebar, proxy, and subnet router you want to use, you need to create a new Tailscale pod running the official Docker image.












### Using Minikube for image build and local development

- https://www.youtube.com/watch?v=_1uWY1GdDVY&ab_channel=GoogleOpenSource


```sh
minikube docker-env
        W0502 10:17:02.728250     12636 main.go:291] Unable to resolve the current Docker CLI context "default": context "default": context not found: open C:\Users\user\.docker\contexts\meta\37a8eec1ce19687d132fe29051dca629d164e2c4958ba141d5f4133a33f0688f\meta.json: The system cannot find the path specified.
        export DOCKER_TLS_VERIFY="1"
        export DOCKER_HOST="tcp://127.0.0.1:57853"
        export DOCKER_CERT_PATH="C:\Users\user\.minikube\certs"
        export MINIKUBE_ACTIVE_DOCKERD="minikube"

# To point your shell to minikube's docker-daemon, run:
# eval $(minikube -p minikube docker-env)


# Now your PC directs to minikube's docker
# From now, Any image you build will be directory on built on minikube's docker

# list images inside minikube cluster
docker images -a

cd dockerfiles
docker build -f dockerfiles/Dockerfile-nginx -t fe-nginx .

```


[↑ Back to top](#)
<br><br>

- deployment.yaml

```yaml
spec:
    templates:
        spec:
            containers:
            - name: fe-nginx
                image: fe-nginx:latest
                ports:
                - containerPort: 80
```

```sh
k apply -f deployment.yaml
```


[↑ Back to top](#)
<br><br>

- suppose source changed -> change image

```sh
docker rmi fe-nginx:latest
docker build -f dockerfiles/Dockerfile-nginx -t fe-nginx .
k delete -f deployment.yaml
k apply -f deployment.yaml
```


[↑ Back to top](#)
<br><br>

- mount data to minikube cluster
    - suppose golang docker container source does:


```go
var version = "0.0.2"
func indexHandler(w http.ResponseWriter, req *http.Request){ 
        // after deployment.yaml volumeMount, this will printout
        // NOTE:
        localFile, err := os.ReadFile("/tmp/data/hello-world.txt")
        if err != nil {
                fmt.Printf("couldn't read file %v\n", err)
        }
        // before deployment.yaml volumeMount, this will printout
        fmt.FPrintf(w,"<h1>hello world :) </h1> \n Version %s\n File Content:%s", version, localFile)
}
```


```sh
minikube mount    {localdir}:{minikube hostdir}

# mount a volume to minikube cluster (persistant storage)
# mount files to minikube cluster
minikube mount    /c/Users/user/Downloads/tmp:/tmp/data
```

```yaml
spec:
    templates:
        spec:
            containers:
            - name: fe-nginx
                image: fe-nginx:latest
                ports:
                - containerPort: 80
                # target dir inside pod: /tmp/data
                volumeMounts:
                - mountPath: /tmp/data
                    name: test-volume
            volumes:
                - name: test-volume
                    # host is kubernetes host(vm)
                    hostPath:
                        # directory location on host
                        path: /tmp/data
```


[↑ Back to top](#)
<br><br>

- apply the changes:

```sh
docker rmi fe-nginx:latest
docker build -f dockerfiles/Dockerfile-nginx -t fe-nginx .
k delete -f deployment.yaml
k apply -f deployment.yaml

# deploy the app
minikube service my-fe-nginx
```

- now edit local hello-world.txt file
- then refresh browser to check the change is immediately applied




[↑ Back to top](#)
<br><br>


- dashboard

```sh
minikube ip
minikube dashboard --url
        http://127.0.0.1:45583/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```


[↑ Back to top](#)
<br><br>

- minikube ingress

https://stackoverflow.com/a/73735009

```sh
# minikube start --cpus 4 --memory 4096
minikube start
minikube addons enable ingress
minikube addons enable ingress-dns

# Wait until you see the ingress-nginx-controller-XXXX is up and running using Kubectl get pods -n ingress-nginx
# Create an ingress using the K8s example yaml file
# Update the service section to point to the NodePort Service that you already created
# Append 127.0.0.1 hello-world.info to your /etc/hosts file on MacOS (NOTE: Do NOT use the Minikube IP)

# ( Keep the window open. After you entered the password there will be no more messages, and the cursor just blinks)
minikube tunnel

# Hit the hello-world.info ( or whatever host you configured in the yaml file) in a browser and it should work
```


[↑ Back to top](#)
<br><br>

Here's a high-level overview of the traffic flow when you access `http://localhost` in your setup:

1. **Browser Request**: When you type `http://localhost` into your browser and hit enter, your browser sends a HTTP request to `localhost`, which is resolved to the IP address `127.0.0.1`.

2. **Port Forwarding**: Since you've set up port forwarding with the command `kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80`, the request to `localhost` on port 80 is forwarded to port 80 on the `ingress-nginx-controller` service.

3. **Ingress Controller**: The Ingress Controller, which is part of the `ingress-nginx-controller` service, receives the request. The Ingress Controller is responsible for routing the request based on the rules defined in your Ingress resource.

4. **Ingress Rules**: In your case, you've set up an Ingress rule to route traffic to the `nginx-service` service on port 80 when the host is `simple-app.com`. However, since you're accessing `localhost` and not `simple-app.com`, this rule does not apply.

5. **Service**: If there were a matching Ingress rule, the Ingress Controller would forward the request to the `nginx-service` service on port 80.

6. **Pod**: The service then load balances the request to one of the pods that match its selector. In your case, this would be the pod running the Nginx application.

Please note that since you're accessing `localhost` and not `simple-app.com`, the Ingress rule does not apply, and the request will not be routed to your Nginx application. To access your application, you need to either use `simple-app.com` as the host or modify your Ingress rule to match `localhost`.



[↑ Back to top](#)
<br><br>

### Microk8s implemntation

- install microk8s (Ubuntu)

```sh
# 1.27/stable version ERROR -> install --classic
sudo snap install microk8s --classic

# 일반유저에게 microk8s 커맨드 권한 부여
# NOTE: root유저로만 microk8s 커맨드 사용시 아래 커맨드 필요 X
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube

microk8s.status --wait-ready
microk8s kubectl get no
microk8s kubectl get svc

cat >> ~/.bashrc <<-EOF

alias k='microk8s.kubectl'
EOF

source ~/.bashrc


microk8s start

# Join node (All 3 are master nodes)
sudo su -
vim /etc/hosts

cat >> /etc/hosts <<-EOF

10.0.2.3 ubuntu-1
10.0.2.4 ubuntu-2
10.0.2.5 ubuntu-3
EOF

# On each vms
ssh foo@10.0.2.3
ssh foo@10.0.2.4
ssh foo@10.0.2.5


# in first node
microk8s add-node

# in other 2 nodes
microk8s join [TOKEN]

# Trouble shoot
# https://microk8s.io/docs/restore-quorum
vim /var/snap/microk8s/current/var/kubernetes/backend/cluster.yaml

- Address: 172.16.9.201:19001
    ID: 3297041220608546238
    Role: 0
- Address: 172.16.9.202:19001
    ID: 13629670026737620399
    Role: 0
- Address: 172.16.9.203:19001
    ID: 10602814967080190144
    Role: 0
```

|<img src="https://d17pwbfgewyq5y.cloudfront.net/microk8s-add-node.png" alt="add-node" width="700">|
|:--:| 
| *Add node to form 3-master-node microk8s cluster* |

|<img src="https://d17pwbfgewyq5y.cloudfront.net/microk8s-3-node.png" alt="3-node" width="450">|
|:--:| 
| *result of a cluster* |



[↑ Back to top](#)
<br><br>

- Trouble-shooting
    - diagnosis:
        - deployed pods with count of 2 replicas, one on node1 and another on node3
        - calling endpoint seems to have different result for each time of calling.
    - cause:
        - microk8s ctr images import was done only one node1.
        - node3 tries to pull image from public docker hub instead of local repository.
        - in result, two pods have different images: one from local repository, another from public docker repository.


|<img src="https://d17pwbfgewyq5y.cloudfront.net/microk8s-cause.png" alt="pods" width="700">|
|:--:| 
| *pod resources* |


```
k describe pod fe-nginx-deployment-7b9c5bb8f8-xlrs2
        Containers:
            fe-nginx:
                Image:                    jnuho/fe-nginx:latest
                Image ID:             sha256:2544d68d372793a21b627c360def55e648ad2cfbbf330a65ba567dbced1985f2

k describe pod fe-nginx-deployment-7b9c5bb8f8-q6d6m
        Containers:
            fe-nginx:
                Image:                    jnuho/fe-nginx:latest
                Image ID:             docker.io/jnuho/fe-nginx@sha256:48e8995cc2c86a3759ac1156cd954d8f90a1c054ae1fcd67181a77df2ff5492f

```


[↑ Back to top](#)
<br><br>

- Local docker registory
    - https://microk8s.io/docs/registry-images

```sh
git clone https://github.com/jnuho/simpledl.git

cd simpledl/script
./1.build-image.sh
./1-1.import-microk8s.sh

docker save jnuho/fe-nginx > fe-nginx.tar
docker save jnuho/be-go > be-go.tar
docker save jnuho/be-py > be-py.tar

microk8s ctr image import fe-nginx.tar
microk8s ctr image import be-go.tar
microk8s ctr image import be-py.tar

rm fe-nginx.tar
rm be-go.tar
rm be-py.tar

microk8s ctr image ls | grep jnuho
```


```sh
microk8s kubectl get pods -A | grep ingress


telnet localhost 8080
telnet localhost 3001
```


[↑ Back to top](#)
<br><br>

- Port forwarding

```
host -> virtualbox vm
```


[↑ Back to top](#)
<br><br>

- ufw setting

```
open port 3001
```



[↑ Back to top](#)
<br><br>

### Pytorch

https://youtu.be/EMXfZB8FVUA?si=XL8SckGQi9xQDgtc
https://pytorch.org/get-started/locally/

- CPU (Without Nvidia CUDA) only

```sh
pip3 install torch torchvision torchaudio

# requirements.txt
torch==2.3.0
torchaudio==2.3.0
torchvision==0.18.0

# install using requirements.txt
python install -r requirements.txt
```

```python
import torch

x = torch.rand(3)
# tensor([.5907, .0781, .3094])
print(x)

print(torch.cuda.is_available())
```


[↑ Back to top](#)
<br><br>


### golang `testing`

```sh
cd leetcode
go test ./...
```

### Crawling

```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gocolly/colly/v2"
)

// problem: 문제번호
// desc: 문제설명
func WriteToFile(problem, desc string) {
	// If the
	fname := "problems/" + problem + ".go"
	f, err := os.OpenFile(fname, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	if _, err := f.Write([]byte(desc)); err != nil {
		f.Close() // ignore error; Write error takes precedence
		log.Fatal(err)
	}
	if err := f.Close(); err != nil {
		log.Fatal(err)
	}
}

// Go Colly (version 2) is a powerful scraping library for Golang,
// but it operates at the HTTP level and can parse static HTML documents.
// Unfortunately, it does not execute JavaScript.
// As a result, it cannot handle Client-Side Rendered (CSR/JS) websites directly.
// When dealing with JavaScript-enabled websites, combine go Colly with a Headless Browser
// https://leetcode.com/api/problems/algorithms/
func main() {
	// Create a new collector
	c := colly.NewCollector(
		// colly.MaxDepth(2),
		colly.Async(true), // Enable asynchronous scraping
	)
	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 2})

	// Set up event listeners

	// Step 1: OnRequest - Called before a request is made
	c.OnRequest(func(r *colly.Request) {
		// Add headers to mimic a browser request
		// r.Headers.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
		r.Headers.Set("User-Agent", "Chrome/125.0.6422.142")
		// You can add mre headers if needed
		fmt.Println("Visiting", r.URL.String())
	})

	c.WithTransport(&http.Transport{
		DisableKeepAlives: true,
	})

	// Step 2: OnError - Called if an error occurs during the request
	c.OnError(func(r *colly.Response, err error) {
		fmt.Println("Request URL:", r.Request.URL, "[status code:", r.StatusCode, "]. failed with response:", string(r.Body), "\nError:", err)
	})

	// Set up event listeners
	// c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
	c.OnHTML("div#qd-content", func(e *colly.HTMLElement) {
		fmt.Println(e)
		// description := e.Attr("content")
		// fmt.Println("Problem description:", description)
	})
	dates := make(chan string)
	titles := make(chan string)
	// Step 3: OnHTML - Called right after OnResponse if the received content is HTML
	// c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
	// c.OnHTML("a.d-block", func(e *colly.HTMLElement) {
	c.OnHTML("div.fight-date", func(e *colly.HTMLElement) {
		// description := e.Attr("content")
		// fmt.Println("Problem description:", description)
		// fmt.Println(len(e))
		dates <- e.Text
		// fmt.Println(e.Text)
	})
	c.OnHTML("div.fight-title", func(e *colly.HTMLElement) {
		// description := e.Attr("content")
		// fmt.Println("Problem description:", description)
		// fmt.Println(len(e))
		titles <- strings.Trim(e.Text, " ")
		// fmt.Println(title)
	})
	// Wait until all threads are finished
	c.Wait()

	// Define the URL to crawl
	// url := "https://leetcode.com/problems/two-sum/description/"
	url := "https://www.boxingscene.com/schedule"

	go func() {
		for title := range titles {
			fmt.Println(title)
		}
		for date := range dates {
			fmt.Println(date)
		}
	}()
	// Start scraping
	c.Visit(url)
	// Now let's use chromedp to get the rendered HTML
	// ctx, cancel := chromedp.NewContext(context.Background())
	// defer cancel()

	// var htmlContent string
	// err := chromedp.Run(ctx,
	// 	// chromedp.Navigate(startURL),
	// 	chromedp.OuterHTML("html", &htmlContent),
	// )
	// if err != nil {
	// 	log.Fatal(err)
	// }

	// Now you can process the rendered HTML using Colly
	// (e.g., extract data from <div> elements, etc.)
	// fmt.Println("Rendered HTML content:", htmlContent)

	// Wait for a few seconds to allow Colly to finish its work
	time.Sleep(5 * time.Second)
	// Write(Append) to file
	//defer WriteToFile(problem, result)
}

```


### AWS go sdk

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/joho/godotenv"
)

func loadEnv() error {
	err := godotenv.Load(".env")
	if err != nil {
		return err
	}
}

func main() {
	// Load .env
	err := loadEnv()
	if err != nil {
		log.Fatalf("Error loading .env file\n")
	}

	// Load AWS SDK configuration
	// sdkConfig, err := config.LoadDefaultConfig(context.TODO())
	sdkConfig, err := config.LoadDefaultConfig(context.TODO(), config.WithSharedConfigProfile("default"))
	if err != nil {
		fmt.Println("Couldn't load default configuration. Have you set up your AWS account?")
		fmt.Println(err)
		return
	}

	// Initialize S3 client
	s3Client := s3.NewFromConfig(sdkConfig)

	// Specify your S3 bucket and image file details
	bucketName := os.Getenv("aws_s3_bucket")
	fileName := "worker_pool_pattern.drawio.png"
	filePath := os.Getenv("aws_s3_local_path") + fileName
	objectKey := fileName

	// Open the local image file
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening local file:", err)
		return
	}
	defer file.Close()

	// Upload the image to S3
	_, err = s3Client.PutObject(context.TODO(), &s3.PutObjectInput{
		Bucket: &bucketName,
		Key:    &objectKey,
		Body:   file,
		// ContentType: aws.String("image/jpeg"), // Set the content type appropriately
		ContentType: aws.String("image/png"), // Set the content type appropriately
	})
	if err != nil {
		fmt.Println("Error uploading image to S3:", err)
		return
	}

	fmt.Println("Image uploaded successfully!")
}

```


[↑ Back to top](#)
<br><br>

### GCP implementation

- Create google account to get free credit for gcloud

- create ubuntu vm
- ip restriction
- install google cloud sdk and init

```sh
gcloud compute security-policies create my-security-policy
gcloud compute security-policies rules create 1000 \
    --security-policy my-security-policy \
    --action allow \
    --src-ip-ranges <your-home-ip>
gcloud compute security-policies rules create 2000 
    --security-policy my-security-policy \
    --action deny \
    --src-ip-ranges 0.0.0.0/0
gcloud compute backend-services update <your-backend-service> \
    --security-policy my-security-policy
```

- GCP console setup
    - vm instacne : create with machine type(E2- memory 4GB)
    - VPC network : firewalls > add filewall rule (your ip)

- gcp ssh connect

```sh
gcloud compute ssh --zone "REGION" "INSTANCE_NAME" --project "PROJECT_NAME"
```



[↑ Back to top](#)
<br><br>


- Google Kubernetes Engine
    - <a href="https://www.youtube.com/watch?v=P1x1Rk_TzV4" target="_blank">Ingress in 5 Minutes</a>
    - <a href="https://youtu.be/8RQvtagsrg0?si=IwP0qNMz0kutUOVo" target="_blank">GKE Load Balancing</a>
    - <a href="https://youtu.be/jW_-KZCjsm0?si=u8-842mszl7O9Kr3" target="_blank">GKE tutorial</a>
    - https://www.youtube.com/watch?v=QvVmQtO-ftU&ab_channel=GoogleCloudTech

- GKE provides a variety of Kubernetes-native constructs to manage L4 and L7 load balancers on Google Cloud.
    - Service, Ingress, Gateway, Network endpoint groups
    - GKE load balancers work by routing traffic to pods based on a set of rules
    - Exposing services outside of the cluster
        - NodePort Service
            - uses GKE Node IP, exposes a service on the "same" port on every Node
        - Load Balancer Service
            - L4 routing (TCP/UDP), allocates a routable IP+port to a Cloud Load Balancer and uses a Node Port to forward traffic to backend pods
        - Ingress/Gateway
            - L7 routing (HTTP/S), allocates a routable IP + HTTP/S ports to a Cloud Load Balancer and uses Pods' IP address to forward traffic directly


0. Create new project and enable Google Kuberentes Engine api

1. Create Kubernetes cluster (console/cli)
    - in console create a cluster
    - 3 nodes, 6CPUs 12 GB

```sh
gcloud container clusters create my-cluster --zone=asia-northeast3-a --num-nodes=3 --machine-type=n1-standard-2

gcloud container clusters list
```

2. Download and install Google Cloud SDK (gcloud)

```sh
gcloud version
gcloud components install kubectl
```

3. Authenticate with gcloud
    - authenticate using your google cloud credentials

```sh
gcloud auth login
```

4. Configure kubectl to Use Your GKE Cluster

```sh
# set the default project for all gcloud commands
gcloud config set project poised-cortex-422112-g5

# Connect to cluster
# `in console 3 dots > Connect` gives a command:
gcloud container clusters get-credentials my-cluster --zone asia-northeast3-a --project poised-cortex-422112-g5
#     > kubeconfig entry generated for my-cluster

# Deploy microservices by creating deployment and service
kubectl create deployment hello-world-rest-api --image=jnuho/fe-nginx:latest

kubectl expose deployment hello-world-rest-api --type=LoadBalancer --port=8080

kubectl get service
    TYPE                 CLUSTER-IP         EXTERNAL-IP
    LoadBalancer 10.80.13.230     <pending>

k get svc --watch
    TYPE                 CLUSTER-IP         EXTERNAL-IP
    LoadBalancer 10.80.13.230     35.184.204.214

curl 35.184.204.214:8080/hello-world
```


[↑ Back to top](#)
<br><br>


- golang cloud library to create VM
    - Create Service account
        - IAM & Admin > Service accounts > Create Service account
            - Assign the `Compute Admin` role
            - click 3 dots for 'Key Management'
            - Create key (JSON) and download and rename `gcp-sa-key.json`
    - Write golang code to execute to create GCP VM.

```
gcp_credential="my-sa-key.json"
gcp_vm_region="asia-northeast3"
gcp_vm_zone="asia-northeast3-a"
gcp_vm_machine_type="e2-medium"
#ubuntu 24.04 50GB
#gcp_vm_boot_disk=50GB
#gcp_vm_identity_and_api_access="Allow full access to all Cloud APIs
#gcp_vm_firewall="http,https,loadbalancer_health_check"
```


- Download Google Cloud SDK and use gcloud to access vm

```sh
gcloud init
gcloud compute ssh instance-20240620-115251 --zone asia-northeast3-a
```

[↑ Back to top](#)
<br><br>

### Github Actions

- `.github/workflows/main.yml`

[↑ Back to top](#)
<br><br>

### golang package

- After updating `pkg/weatherapi.go`
    - only have to go mod init the project `github.com/jnuho/simpledl`
    - then any sub-project can be accessed as :
        - `github.com/jnuho/simpledl/pkg`
        - `github.com/jnuho/simpledl/backend/web`

[↑ Back to top](#)
<br><br>

### Writing Dockerfile

- https://docs.docker.com/reference/dockerfile/



[↑ Back to top](#)
<br><br>



### AWS EKS with terraform

- [`LINK`](https://blogd.org/blog/2024/06/25/eks-with-terraform)
