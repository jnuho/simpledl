# Simple Deep learning application

[Deep learning](#https://en.wikipedia.org/wiki/Deep_learning) is an algorithm inspired by how 🧠 works. It distinguishes itself in the identification of patterns across various forms of data, including but not limited to images, text, and sound. It uses forward and backward propagation to find parameters (weights and biases) that minimize the cost function, which is a metric that measures how far off its predictions are from the actual answer(label).

> I created two simple deep learning models to identify cat images and hand-written digits (0-9), respectively.

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



### Minikube deployement

To set up your Nginx, Golang, and Python microservices on Minikube, you'll need to create Kubernetes Deployment and Service YAML files for each of your microservices. You'll also need to set up an Ingress controller to expose your services to the public. Here's a high-level overview of the steps:

1. **Install Minikube**: If you haven't already, you'll need to install Minikube on your machine. Minikube is a tool that lets you run Kubernetes locally.

2. **Start Minikube**: Once installed, you can start a local Kubernetes cluster with the command `minikube start`.

3. **Enable Ingress Controller**: To set up the Ingress controller on Minikube, you can use the command `minikube addons enable ingress`¹[5].

4. **Create Deployment and Service YAML Files**: For each of your microservices (Nginx, Golang, Python), you'll need to create a Deployment and a Service. The Deployment defines your application and the Docker image it uses, while the Service defines how your application is exposed to the network²[1]. 

5. **Apply the YAML Files**: Once you've created your YAML files, you can apply them to your Kubernetes cluster with the command `kubectl apply -f <filename.yaml>`.

6. **Create an Ingress YAML File**: The Ingress YAML file will define the rules for routing external traffic to your services. You'll need to specify the host and path for each service, and the service that should handle traffic to each host/path¹[5].

7. **Apply the Ingress YAML File**: Just like with the Deployment and Service files, you can apply the Ingress file with `kubectl apply -f <ingress-filename.yaml>`.

8. **Access Your Services**: With the Ingress set up, you should be able to access your services from outside your Kubernetes cluster. You can get the IP address of your Minikube cluster with the command `minikube ip`, and then access your services at that IP¹[5].

Remember, these are just high-level steps. The exact details may vary depending on your specific microservices and configuration. Let me know if you need more detailed guidance on any of these steps! 😊

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