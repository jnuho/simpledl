# Simple Deep learning application

[Deep learning](#https://en.wikipedia.org/wiki/Deep_learning) is an algorithm inspired by how 🧠 works. It distinguishes itself in the identification of patterns across various forms of data, including but not limited to images, text, and sound. It uses forward and backward propagation to find parameters (weights and biases) that minimize the cost function, which is a metric that measures how far off its predictions are from the actual answer(label).

> I created two simple deep learning models to identify cat images and hand-written digits (0-9), respectively.

## Microservices

https://fastapi.tiangolo.com/tutorial/
fastapi + docker + minikube + k8s service + k8s ingress with nginx

1. frontend: nodejs + javascript + html + css
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


### Typescript (optional)

- Download  & install nodejs 20.12.2

```sh
npm create vite@latest
  ? Project name: lesson11
  > choose Vanilla, TypeScript
```

- Edit `package.json` to edit port and dependencies

```json
  "scripts": {
    "dev": "vite --port 4200",
  },

  "dependencies": {
    "axios": "^1.6.8"
  }
```

### Node server

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

- frontend node


```Dockerfile
```