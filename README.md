# Simple Deep learning application

I implemented a simple MSA service - nginx, golang, python. I tried to use docker-compose.yaml for **docker** implementation and then **minikube** to deploy a single node cluster in local environment. My simple application is a basic deep learning image recognizer exercises, one of which was covered in Andrew Ng's coursera course. I created two simple deep learning models to identify cat images and hand-written digits (0-9), respectively.

**[Deep learning](#https://en.wikipedia.org/wiki/Deep_learning)** is an algorithm inspired by how 🧠 works. It distinguishes itself in the identification of patterns across various forms of data, including but not limited to images, text, and sound. It uses forward and backward propagation to find parameters (weights and biases) that minimize the cost function, which is a metric that measures how far off its predictions are from the actual answer(label).

## Microservices

https://fastapi.tiangolo.com/tutorial/
fastapi + docker + minikube + k8s service + k8s ingress with nginx

1. frontend: nginx (nodejs vite in local) + javascript + html + css
2. backend/web: golang (gin framework)
3. backend/worker: python (fast api, numpy, scikit-learn)


### Communication between services

- REST API
  - Javascript &rarr; Golang
- GRPC
  - Golang &harr; python

I considered various communication method:

There are several ways to enable communication between a Golang web server and a Python backend. Here are a few methods:

1. **HTTP/REST API**: You can expose a REST API on your Python backend and have the Golang server make HTTP requests to it. This is similar to how your JavaScript frontend communicates with the Golang server¹.

2. **gRPC/Protobuf**: gRPC is a high-performance, open-source universal RPC framework, and Protobuf (short for Protocol Buffers) is a method for serializing structured data. You can use gRPC and Protobuf for communication between your Golang and Python applications¹. This method is efficient and type-safe, but it might be a bit more complex to set up compared to a REST API¹.

3. **Message Queue**: If your use case involves asynchronous processing or you want to decouple your Golang and Python applications, you can use a message queue like RabbitMQ or Apache Kafka. In this setup, your Golang application would publish messages to the queue, and your Python application would consume these messages³.

4. **Socket Programming**: You can use sockets for communication if both your Golang and Python applications are running on the same network³. This method requires a good understanding of network programming³.

5. **Database**: If both applications have access to a shared database, you can use the database as a communication medium. One application writes to the database, and the other one reads from it².



### Prerequisite for microsservices

- [CORS issue](#https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
	- when a web application tries to make a request to a server that’s on a different domain, protocol, or port, it encounters a CORS (Cross-Origin Resource Sharing) issue

```
For security reasons, browsers restrict cross-origin HTTP requests initiated from scripts. For example, fetch() and XMLHttpRequest follow the same-origin policy.

This means that a web application using those APIs can only request resources from the same origin the application was loaded from unless the response from other origins includes the right CORS headers.

-> Add appropriate headers in golang server.
```


### Backend - gin server (golang)


```sh
cd simpledl/backend/web

go mod init github.com/jnuho/simpledl/backend/web

# download library dependencies specified in main.go
go mod tidy
```

### Backend - Python Fast API and Uvicorn web server

- Use FastAPI + Unicorn
  - FastAPI is an ASGI (<b>Asynchronous</b> Server Gateway Interface) framework which requires an ASGI server to run.
  - Unicorn is a lightning-fast ASGI server implementation


- install python (download .exe from python.org)
  - check Add to PATH option (required)


- `.tmux.conf`

https://unix.stackexchange.com/a/669231
https://github.com/tmux-plugins/tmux-yank

```
# NOTE: to apply the changes:
# tmux source-file .tmux.conf

unbind C-b
set -g prefix C-a

# SELECT
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D


# RESIZE by {5}
bind -n M-S-Left resize-pane -L 3
bind -n M-S-Right resize-pane -R 3
bind -n M-S-Up resize-pane -U 3
bind -n M-S-Down resize-pane -D 3

# SWAP
bind -n C-S-Up swap-pane -U
bind -n C-S-Down swap-pane -D

set -g mouse on

set -g default-terminal "screen-256color"

run-shell ~/clone/path/yank.tmux
```

```sh
cd ~
git clone https://github.com/tmux-plugins/tmux-yank ~/clone/path

# type this inside tmux
tmux source-file ~/.tmux.conf
```

- `requirements.txt`

```
numpy==1.26.4
h5py==3.10.0
matplotlib==3.8.3
scipy==1.12.0
pillow==10.2.0
imageio==2.34.0
scikit-image==0.23.1

fastapi==0.110.2
pydantic==2.7.1
pydantic_core==2.18.2

uvicorn==0.29.0

keyboard==0.13.5
mouse==0.7.1
PyAutoGUI==0.9.54
PyGetWindow==0.0.9
pynput==1.7.6
PyScreeze==0.1.30
opencv-python==4.9.0.80
pywinauto==0.6.8
```

- `.bashrc`

```
# Use python in .venv install for simpledl workspace
alias python='winpty /c/Users/user/Repos/simpledl/.venv/Scripts/python.exe'
alias pip='winpty /c/Users/user/Repos/simpledl/.venv/Scripts/pip.exe'
alias uvicorn='winpty /c/Users/user/Repos/simpledl/.venv/Scripts/uvicorn.exe'
alias tmux='tmux -2'
```


- Run the python web server

```sh
uvicorn main:app --port 3002
```


#### Mathematical operations for deep learning

The basic operations for forward and backward propagations in deep learning algorithm are as follows:

- Forward propagation for layer $l$: $a^{[l-1]}\rightarrow a^{[l]}, z^{[l]}, w^{[l]}, b^{[l]}$

  $Z^{[l]} = W^{[l]} A^{[l-1]} + b^{[l]}$

  $A^{[l]} = g^{[l]} (Z^{[l]})$

  (for $i=1,\dots,L$ with initial value $A^{[0]} = X$)

- Backward propagation for layer $l$: $da^{[l]} \rightarrow da^{[l-1]},dW^{[l]}, db^{[l]}$

  $dZ^{[l]} = dA^{[l]} * {g^{[l]}}^{'}(Z^{[l]})$

  $dW^{[l]} = \frac{1}{m}dZ^{[l]}{A^{[l-1]}}^T$

  $db^{[l]} = \frac{1}{m}np.sum(dZ^{[l]}, axis=1, keepdims=True)$

  $dA^{[l-1]} = {W^{[l]}}^T dZ^{[l]} = \frac{dJ}{dA^{[l-1]}} = \frac{dZ^{[l]}}{dA^{[l-1]}} \frac{dJ}{dZ^{[l]}} = \frac{dZ^{[l]}}{dA^{[l-1]}} dZ^{[l]}$

  (with initial value $dZ^{[L]} = A^{[L]}-Y$)


### Frontend local setup

- Download  & install nodejs 20.12.2
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

### Node server

Note that I will be using nginx instead in production environment. I used nodejs vite for local development environment for convenience.

```sh
# install dependencies specified in package.json
# install if package.json changes e.g. project name
npm i
npm run dev
  VITE v5.2.9  ready in 180 ms

  ➜  Local:   http://localhost:4200/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

- Edit code
  - Write `index.html`
  - Create directory: `./model`, `./templates`
  - Define models and templates
  - Edit `main.ts`



## Dockerize


```
Important Reminder: It is crucial to optimize Docker images to be as compact as possible. One strategy to achieve this is by utilizing base images that are minimalistic, such as the Alpine image.
```

- [NOTE on defining backend endpoint in frontend](https://stackoverflow.com/a/56375180/23876187)
  - frontend app is not in any container, but the javascript is served from container as a js script file to <b>your browser</b>!

- frontend nginx service

```Dockerfile
```


curl -X POST -H "Content-Type: application/json" -d '{"cat_url":"aa"}' http://backend_python:3002/worker/cat


### Nginx lua module


Nginx Lua is a module for Nginx that embeds Lua, a lightweight and powerful scripting language, directly into Nginx.

The use of OpenResty and Lua is not necessary if you don't have any dynamic content or complex logic that needs to be executed at the Nginx level. The power of OpenResty and Lua comes into play when you need to perform operations that are beyond the capabilities of standard Nginx configuration.

Here are a few examples of what you can do with Lua in Nginx:

1. **Dynamic Routing**: You can use Lua to dynamically determine where to route requests based on complex logic that can't be expressed in standard Nginx configuration.

2. **Advanced Caching**: While Nginx has built-in caching, Lua allows you to implement more advanced caching strategies. For example, you could cache responses in a Redis database and use Lua to fetch and update these cached responses.

3. **Custom Authentication**: You can use Lua to implement custom authentication mechanisms. For example, you could use Lua to validate JSON Web Tokens (JWTs) or to implement OAuth 2.0.

4. **Complex Load Balancing**: While Nginx supports basic load balancing, Lua allows you to implement more complex load balancing algorithms.

5. **Real-time Metrics and Monitoring**: You can use Lua to collect real-time metrics about your requests and responses, which can be useful for monitoring and debugging.

6. **Modifying Requests and Responses**: Lua can be used to modify both incoming requests and outgoing responses. This can be useful for a variety of purposes, such as adding or modifying headers, rewriting URLs, or transforming response bodies.

If your use case doesn't require any of these features, then you might not need to use Lua with Nginx. However, if you anticipate needing these features in the future, it could be beneficial to start with OpenResty and Lua from the beginning.


### Docker install (ubuntu 24.04)


- https://docs.docker.com/engine/install/ubuntu/

```sh
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done


# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Manage Docker as a non-root user
# https://docs.docker.com/engine/install/linux-postinstall/

sudo groupadd docker
sudo usermod -aG docker $USER

# Log out and log back in so that your group membership is re-evaluated.
# You can also run the following command to activate the changes to groups:
newgrp docker
```

### Minikube deployement

To set up your Nginx, Golang, and Python microservices on Minikube, you'll need to create Kubernetes Deployment and Service YAML files for each of your microservices. You'll also need to set up an Ingress controller to expose your services to the public. Here's a high-level overview of the steps:

1. **Install Minikube**: If you haven't already, you'll need to install Minikube on your machine. Minikube is a tool that lets you run Kubernetes locally.

- ubuntu 24.04 install minikube

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb
```

2. **Start Minikube**: Once installed, you can start a local Kubernetes cluster with the command `minikube start`.

```sh
# As a TROUBLE SHOOTING:
docker context use default
  default
  Current context is now "default"

minikube start
```

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
  #   must be matched by service.yaml > spec.selector
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


5. **Apply the YAML Files**: Once you've created your YAML files, you can apply them to your Kubernetes cluster with the command `kubectl apply -f <filename.yaml>`.


6. **Enable Ingress Controller**:

6-1. (NOT WORKING: check 3-2 instead) NGINX ingress controller using Minikube addons: you can use the command `minikube addons enable ingress`

```sh
minikube addons enable ingress
```

6-2. (USE THIS!) Nginx ingress controller

- [setting up an NGINX ingress controller](#https://medium.com/@amirhosseineidy/how-to-set-up-nginx-ingress-controller-in-local-server-6cc4bd7d6a6b) in a bare metal or local server:


Ingress is an API in Kubernetes that routes traffic to different services, making applications accessible to clients from the Kubernetes cluster. Among multiple choices like HAProxy or Envoy for setting up an ingress controller, NGINX is the most popular one. It is powered by the NGINX web server and is a fast and secure controller that delivers your applications to the clients easily.

- Install NGINX ingress controller with `helm`

```sh
# inside cmd or powershell
winget install Helm.Helm

# RESTART terminal
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx
```

- Check if ingress controller is working:

```sh
helm list
  NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
  ingress-nginx   default         1               2024-04-30 14:26:18.9350713 +0900 KST   deployed        ingress-nginx-4.10.1    1.10.1

k get ClusterRole | grep ingress
  ingress-nginx                                                          2024-04-30T07:01:05Z

k get all
  NAME                                           READY   STATUS    RESTARTS   AGE
  pod/ingress-nginx-controller-cf668668c-zvkd9   1/1     Running   0          44s

  NAME                                         TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
  service/ingress-nginx-controller             LoadBalancer   10.100.168.236   <pending>     80:32020/TCP,443:31346/TCP   44s
  service/ingress-nginx-controller-admission   ClusterIP      10.107.208.79    <none>        443/TCP                      44s
  service/kubernetes                           ClusterIP      10.96.0.1        <none>        443/TCP                      4m8s

  NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
  deployment.apps/ingress-nginx-controller   1/1     1            1           44s

  NAME                                                 DESIRED   CURRENT   READY   AGE
  replicaset.apps/ingress-nginx-controller-cf668668c   1         1         1       44s
```


7. **Create an Ingress YAML File**: The Ingress YAML file will define the rules for routing external traffic to your services. You'll need to specify the host and path for each service, and the service that should handle traffic to each host/path

8. **Apply the Ingress YAML File**: Just like with the Deployment and Service files, you can apply the Ingress file with `kubectl apply -f <ingress-filename.yaml>`.

- Ingress rules
  - Ingress rules are resources that help route services to your desired domain name or prefix. They are divided into prefix and DNS.
  - .yaml mainifest for ingress rules

```sh
k apply ingress.yaml
k get ingress
  NAME               CLASS   HOSTS                ADDRESS        PORTS   AGE
  fe-nginx-ingress   nginx   my-app.example.com   192.168.49.2   80      4m35s
```


9. **Access Your Services**: With the Ingress set up, you should be able to access your services from outside your Kubernetes cluster. You can get the IP address of your Minikube cluster with the command `minikube ip`, and then access your services at that IP


- Accessing application
  - For accessing these applications in a local cluster, you should access it through node port (30000 ports) or use a reverse proxy to send them.
  - But is there any way to access app on port 80 or 443?
    - use Port-forward or `MetalLB` to allow access to app on port 80 or 443.

- port forward

```sh
kubectl port-forward --address 0.0.0.0 svc/fe-nginx-service 8080:80
```

- Installing Metallb

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
  NAME                          READY   STATUS    RESTARTS   AGE
  controller-596589985b-jrnmk   1/1     Running   0          34m
  speaker-hdrmc                 4/4     Running   0          34m
```

- Now set a range IPs for your local load balancer by creating a configMap. 
  - Remember that the set of IP addresses you apply must be in the same range as your nodes IPs

The range of IP addresses you choose for MetalLB should be in the same subnet as your nodes' IPs. These IP addresses are used by MetalLB to assign to services of type LoadBalancer.
Using command, `k get node -o wide`, the INTERNAL-IP of my node is 192.168.49.2. So, choose a range of IP addresses in the 192.168.49.x range for MetalLB. For example, 192.168.49.100-192.168.49.110 as my range.

The IP addresses you choose for MetalLB should be reserved for MetalLB's use and should not conflict with any other devices on your network.

```yaml
# to see ip range for node
kubectl get nodes -o wide
  NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION                       CONTAINER-RUNTIME
  minikube   Ready    control-plane   41m   v1.30.0   192.168.49.2   <none>        Ubuntu 22.04.4 LTS   5.15.146.1-microsoft-standard-WSL2   docker://26.0.1

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
  NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)                      AGE
  ingress-nginx-controller             LoadBalancer   10.100.168.236   192.168.49.100   80:32020/TCP,443:31346/TCP   68m
```

- DNS Setup
  - Finally, you need to set the domain names defined in the ingress rules in your DNS server or hosts file
  - edit hosts file, `C:\Windows\System32\drivers\etc\hosts`

```
192.168.49.100 my-app.example.com
```


(1) Set up Ingress on Minikube with the NGINX Ingress Controller. https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/.
(2) Kubernetes Deployment YAML File with Examples. https://spacelift.io/blog/kubernetes-deployment-yaml.
(3) Kubernetes YAML Generator. https://k8syaml.com/.
(4) How to create Kubernetes YAML files | HackerNoon. https://hackernoon.com/how-to-create-kubernetes-yaml-files.
(5) How To Create Kubernetes YAML Manifests Quickly - DevOpsCube. https://devopscube.com/create-kubernetes-yaml/.
(6) Setting up Ingress on Minikube - Medium. https://medium.com/@Oskarr3/setting-up-ingress-on-minikube-6ae825e98f82.
(7) How to Setup NGINX Ingress Controller in Kubernetes - LinuxTechi. https://www.linuxtechi.com/setup-nginx-ingress-controller-in-kubernetes/.
(8) Minikube with ingress example not working - Stack Overflow. https://stackoverflow.com/questions/58561682/minikube-with-ingress-example-not-working.
(9) How to Setup Ingress on Minikube Kubernetes with example - Geeks Terminal. https://geeksterminal.com/setup-ingress-on-minikube-for-kubernetes/2972/.
(10) How to Run Nginx on Kubernetes Using Minikube | Cloud Native Daily - Medium. https://medium.com/cloud-native-daily/how-to-run-nginx-on-kubernetes-using-minikube-df3319b80511.
(11) NGINX Tutorial: How to Deploy and Configure Microservices. https://www.nginx.com/blog/nginx-tutorial-deploy-configure-microservices/.
(12) Kubernetes for Beginners: Nginx Deployment with Minikube. https://techbeats.blog/kubernetes-for-beginners-nginx-deployment-with-minikube.
(13) undefined. https://kubernetes.io/docs/tasks/tools/.
(14) undefined. http://www.sandtable.com/a-single-aws-elastic-load-balancer-for-several-kubernetes-services-using-kubernetes-ingress/.
(15) undefined. https://gist.github.com/0sc/77d8925cc378c9a6a92890e7c08937ca.




### Using Minikube for image build and local development

- https://www.youtube.com/watch?v=_1uWY1GdDVY&ab_channel=GoogleOpenSource


```sh
minikube docker-env
$ minikube docker-env
    W0502 10:17:02.728250   12636 main.go:291] Unable to resolve the current Docker CLI context "default": context "default": context not found: open C:\Users\user\.docker\contexts\meta\37a8eec1ce19687d132fe29051dca629d164e2c4958ba141d5f4133a33f0688f\meta.json: The system cannot find the path specified.
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

- suppose source changed -> change image

```sh
docker rmi fe-nginx:latest
docker build -f dockerfiles/Dockerfile-nginx -t fe-nginx .
k delete -f deployment.yaml
k apply -f deployment.yaml
```

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
minikube mount  {localdir}:{minikube hostdir}

# mount a volume to minikube cluster (persistant storage)
# mount files to minikube cluster
minikube mount  /c/Users/user/Downloads/tmp:/tmp/data
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



### GCP test

- create ubuntu vm
- ip restriction


- install google cloud sdk and init

```sh
```



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

- dashboard

```sh
minikube ip
minikube dashboard --url
    http://127.0.0.1:45583/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

- minikube ingress

https://stackoverflow.com/a/73735009

```sh
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


- GCP console setup
  - vm instacne : create with machine type(E2- memory 4GB)
  - VPC network : firewalls > add filewall rule (your ip)

- gcp ssh connect

```sh
gcloud compute ssh --zone "REGION" "INSTANCE_NAME" --project "PROJECT_NAME"
```


