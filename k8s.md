
### Kubernetes Core Concept

While I've been using `kubectl` commands to manage services in a cluster; creating ingress, service, pod components, etc, I've been lacking deeper knowledge of what they are, how they are interconnected and how clients access the cluster via endpoints. So I tried to understand the concept of each component.

- <a href="https://kubernetes.io/docs/concepts/overview/components/" target="_blank">Kubernetes doc</a>
- <a href="https://youtu.be/s_o8dwzRlu4?si=cz3-XlNOq91CUyz8&t=104">Kubernetes by Nana-1hr</a>
- <a href="https://www.youtube.com/watch?v=X48VuDVv0do&t=1594s&ab_channel=TechWorldwithNana" target="_blank">Kuberentes by Nana-3hr</a>
- <a href="https://medium.com/devops-mojo/kubernetes-objects-resources-overview-introduction-understanding-kubernetes-objects-24d7b47bb018" target="_blank">Kubernetes — Objects</a>


|<img src="https://kubernetes.io/images/docs/components-of-kubernetes.svg" alt="add-node" width="820">|
|:--:| 
| *components-of-kubernetes* |

- Master node
  - runs the control plane components, monitor and manage overall state of the cluster and resources
  - schedule and start pods
  - 4 processes run on every master node:
  - `kube-apiserver`
    - exposes the Kubernetes API and provides the front end to the Control Plane.
    - a single entrypoint (cluster gateway) for interacting with the k8s control plane
    - handles api requests, authentication, and authorization
    - acts as a gatekeeper for authentication
      - request → api server → validates request → other processes → pod creation
    - UI (dashboard), API(script,sdk), CLI (kubectl)
  - `kube-scheduler`
    - schedule new pod → api server → scheduler
    - → intelligently decide which node to put the new Pods based on resource percentage of nodes being used
    - scans for newly created pods and assigns them nodes based on a variety of factors
      - including resource requirements, hardware/software constraints and data locality.
    - distribute workloads across worker nodes
  - `kube-controller-manager`
    - ensures the cluster remains in the desired state
    - run controllers which run loops to ensure the configuration matches actual state of the running cluster.
    - these controllers are as follows:
      - Node controller — Checks and ensures nodes are up and running
      - Job Controller — Manages one-off tasks
      - Endpoints Controller — Populates endpoints and joins services and pods.
      - Service Account and Token Controller — Creation of accounts and API Access tokens.
    - detect cluster state changes(pods state)
    - Controller Manager(detect pod state) → Scheduler → Kublet(on worker node)
  - `cloud-controller-manager`
  - `etcd`
    - consistent and highly-available key-value store that maintains cluster state and ensures data consistency
    - cluster brain!
    - key-value data store of cluster state
    - cluster changes get stored in the key value store!
    - Is the cluster healthy? What resources are available? Did the cluster state change?
    - NO application data is stored in etcd!
    - can be replicated
    - Multiple master nodes for secure storage
      - api server is load balanced
      - distributed storage across all the master nodes
- Worker node
  - host multiple pods which are the components of the application workload
  - the following 3 processes must be installed on every node:
  - `kubelet`
    - schedules pods and containers
    - interacts with both the container and node
    - starts the pod with a container inside
    - agent running on each node
    - watches for changes in pod spec and takes action
    - ensures the pods running on the node are running and are healthy.
  - `kube-proxy`
    - forwards requests to services to pods
    - intelligent and performant forwarding logic that distributes request to pods with low network overhead
      - it can forward pod request for a service into the pod in the same node instead of forwarding to pods in other nodes, therefore lowers possible network overhead.
    - a daemon on each node that allows network rules such as load balancing and routing
    - enables communication between pods and external clients
    - Proxy network running on the node that manage the network rules
    - and communication across pods from networks inside or outside of the cluster.
  - `Container runtime`
    - responsible for pulling images, creating containers
    - e.g. containerd

- https://kubernetes.io/docs/concepts/architecture/

|<img src="https://kubernetes.io/images/docs/kubernetes-cluster-architecture.svg" alt="add-node" width="820">|
|:--:| 
| *kubernetes-cluster-architecture* |


- Example of Cluster Set-up
  - 2 Master nodes, 3 Worker nodes
  - Master node : less resources
  - Worker node : more resources for running applications
  - can add more Master or Worker nodes

- Pod
  - "Pods are the smallest deployable units of computing that you can create and manage in Kubernetes."
  - abstraction over container
  - usually 1 application(container) per pod
  - each pod gets its own ip address
  - ephermeral; new (unique) ip for each re-creation

- Service
  - <a href="https://youtu.be/s_o8dwzRlu4?si=JA5oLELcsrNUdCYn&t=739" target="_blank">Service & Ingress</a>
  - Service provide stable(permanent) IP address. Each pod has its own ip address, but are ephemeral.
  - Load balancing
  - loose coupling
  - within & outside cluster
  - pods communite with each other using services
  - external service
    - http://node-ip:port
  - internal service
    - http://db-service-ip:port

- ClusterIP services
  - default type
  - microservice app deployed

- Ingress
  - https://www.youtube.com/watch?v=NPFbYpb0I7w&ab_channel=IBMTechnology
  - https://youtu.be/80Ew_fsV4rM?si=xAS60zSQzhhAEcnb
  - https://youtu.be/X48VuDVv0do?si=K1BDcMdSDNyIK1Ck&t=7312
  - https://www.youtube.com/watch?v=y5-u4jtflic&ab_channel=TTABAE-LEARN
  - <a href="https://youtu.be/s_o8dwzRlu4?si=JA5oLELcsrNUdCYn&t=739" target="_blank">Service & Ingress</a>
  - `https://my-app.com` (ingress can configure secure https protocal with domain name) → forwards traffic into `internal` service
  - [ingress by traefik.io](https://traefik.io/glossary/kubernetes-ingress-and-ingress-controller-101/#:~:text=A%20Kubernetes%20ingress%20controller%20follows,state%20requested%20by%20the%20user)
  - [gke ingress](https://thenewstack.io/deploy-a-multicluster-ingress-on-google-kubernetes-engine/?ref=traefik.io)
  - [load balancer and ingress duo](https://medium.com/@rehmanabdul166/explaining-load-balancers-and-ingress-controller-a-powerful-duo-bca7add558ab)
  - [load balancer vs. ingress](https://medium.com/@thekubeguy/load-balancer-vs-ingress-why-do-we-need-both-for-same-work-3ae2b9afdd5a)

- Let's walk through the flow of traffic in a Kubernetes environment with:
  - Ingress
  - Ingress Controller
  - external Load Balancer (such as an Application Load Balancer, ALB):

1. **Ingress Creation**:
   - You start by creating an Ingress resource in your Kubernetes cluster.
   - The Ingress defines routing rules based on HTTP hostnames and URL paths.

2. **External Load Balancer (ELB) Creation**:
   - When you create an Ingress, the cloud environment (e.g., AWS) automatically provisions an external Load Balancer (e.g., ALB).
   - The ELB acts as the entry point for external traffic.

3. **Traffic Flow**:
   - Here's how the traffic flows:
     - **External Client**: Sends a request to the ALB (Load Balancer).
     - **ALB**: Receives the request and forwards it to the Ingress Controller.
     - **Ingress Controller**: Based on the Ingress rules, the controller routes the request to the appropriate Kubernetes Service.
     - **Service**: The Service forwards the request to the corresponding Pod(s).

So, the complete flow is: **ALB → Ingress Controller → Ingress → Service → Pod**.

Ingress allows fine-grained routing, and the Ingress Controller ensures that the load balancer routes requests correctly. If you need more complex routing based on HTTP criteria, Ingress is a powerful tool! 🚀


1. Use External Service: http://my-node-ip:svcNodePort → Pod
  - service.spec.type=LoadBalancer, nodePort=30510
  - http://localhost:30510/
    - in VirtualBox port-forward 30510
2. Use `Ingress` + Internal service: https://my-app.com
  - Ingress Controller Pod → Ingress (routing rule) → Service → Pod
  - using ingress, you can configure https connection


### Ingress Explained

1. External Service (without Ingress)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-external-service
spec:
  selector:
    app: myapp
  # LoadBalancer : opening to public
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30510
```

2. Using Ingress → internal Service (e.g. `myapp-internal-service`)
  - internal service has no `nodePort` and the type should be `type: ClusterIP`
  - must be valid domain address
  - map domain name to Node's IP address, which is the entrypoint
    - (one of the nodes or could be a host machine outside the cluster)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp-com
    http:
      # incoming requests are forwarded to the internal service
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-internal-service
            port: 8080

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-internal-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
```

- Ingress controller
  - implementation of ingress, which is Ingress Controller (Pod)
  - evaluates and processes ingress rules
  - manages redirections
  - entrypoint to cluster
  - many third party implementations
    - e.g. k8s Nginx Ingress Controller
  - HAVE TO CONSIDER the environemnt where the k8s cluster is running
    - Cloud Service Provider (AWS, GCP, AZURE)
      - External reqeust from the browser →
        - Cloud Load balancer →
        - Ingress Controller Pod →
        - Ingress →
        - Service →
        - Pod
      - using cloud lb, you do not have to implement load balancer yourself
    - Baremetal
      - you need to configure some kind of entrypoint (e.g. metallb)
      - either inside of cluster or outside as separate server
      - software or hardware solution can be used
      - must provide entrypoint
      - e.g. Proxy Server: public ip address and open ports
        - Proxy server → Ingress Controller Pod → Ingress (checks ingress rules) → Service → Pod
        - no server in k8s cluster is publicly accessible from outside


- Minikube ingress implementation

```sh
# nginx implementation of ingress controller
minikube addons enable ingress

k get pod -n kube-system
  nginx-ingess-controller-xxx

```

- configure ingress rule for kubernetes dashboard componnent
  - minikube in default creates dashboard service (minikube specific)

```sh
k get ns
  kubernetes-dashboard Active 17d

k get all -n kubernetes-dashboard
  pod
  svc
```

- dashboard-ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dashboard-ingress
  namespace: kubernetes-dashboard
spec:
  rules:
  - host: dashboard.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            # forward to service name created in minikube
            name: kubernetes-dashboard
            port:
              number: 80
```

- create ingress rule for kubernetes-dashboard

```sh
k apply -f dashboard-ingress.yaml

k get ingress -n kubernetes-dashboard --watch
  NAME               CLASS   HOSTS             ADDRESS        PORTS   AGE
  dashboard-ingress  nginx   dashboard.com     192.168.49.2   80      42s

vim /etc/hosts
  192.168.49.2 dashboard.com

# check in chrome browser:
# http://dashboard.com

k describe ingress dashboard-ingress -n kubernetes-dashboard

  # whenever there's a request into the cluster, there's no rule for mapping the request to service, then
  # this backend is default to handle the request. e.g. 404 not found
  # one can define custom error page
  # SIMPLY CREATE A SERVICE WITH THE SAME NAME: default-http-backend
  Default backend: default-http-backend:80
```

- Define custom `default-http-backend`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: default-http-backend
spec:
  selector:
    app: default-response-app
  ports:
    - protocol: TCP
      # this is the port that receives the default backend response
      port: 80
      targetPort: 8080
```

- ingress rules

- multiple paths for the same host
  - http://myapp.com/analytics
  - http://myapp.com/shopping

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-fanout-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.com
    http:
      paths:
      - path: /analytics
        pathType: Prefix
        backend:
          service:
            name: analytics-service
            port:
              number: 3000
      - path: /shopping
        pathType: Prefix
        backend:
          service:
            name: shopping-service
            port:
              number: 8080
```


- multiple hosts
  - http://analytics.myapp.com
  - http://shopping.myapp.com

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-fanout-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: analytics.myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: analytics-service
            port:
              number: 3000
  - host: shopping.myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: shopping-service
            port:
              number: 8080
```


- Ingress that includes configuration of TLS certificate
  - Secret component : define yaml to create one
    - tls.crt, tls.key : values are actual file contents, NOT file paths/locations
    - Secret must bein the same namepsace as the Ingress Component

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-example-ingresss
spec:
  ########## TLS SETTING ##########
  tls:
  - hosts:
    - myapp.com
    secretName: myapp-secret-tls
  ########## TLS SETTING ##########
  rules:
  - host: myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-internal-service
            port:
              number: 8080
---
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret-tls
  namespace:default
data:
  tls.crt: base64 encoded cert
  tls.key: base64 encoded key
type: kubernetes.io/tls
```



- ConfigMap
  - stored in plaintext format
  - external configuration of your application
  - `DB_URL = monngo-db`

- Secret
  - Caution: "Kubernetes Secrets are, by default, stored unencrypted in the API server's underlying data store (etcd)."
    - https://kubernetes.io/docs/concepts/configuration/secret/
  - stored in base64 encoded format
  - `DB_USER = mongo-user`
  - `DB_PW = mongo-pw`

- Volume (like an external hdd plugged into cluster)
  - k8s does not manage data persistence
  - if database pod dies the data disappears
  - it requires persistent database
  - strorage could on:
    - on Local
    - on Remote, outside of the cluster


- What if pod dies => downtime occurs.
  - use service as a load balancer which distributes traffic to multiple nodes
  - Use multi-node and pod replicas(deployment as abstraction for pods)
  - deployment specifies how many pods are deployed into multiple nodes
  - BUT, database pods cannot be replicated. it requires to store data into a single storage
    - use StatefulSet for stateful apps such as Databases

- `Deployemnt` for stateless apps
  - Deployment is the Abstraction of Pods

- `StatefulSet` for stateFul apps or databases
  - DB can't be replicated via deployment.
  - Avoid data inconsistencies
  - => StatefulSet for STATEFUL apps. e.g. mysql, mongodb, elastic search
  - But deploying StatefulSet is not easy
  - `NOTE`: "DB are often hosted outside of k8s cluster"

- Minikube
  - master and worker process run on a single node
  - usually via virtual box or other hypervisor
  - for testing purposes

- deployment
  - blueprint for creating pods
  - most basic configuration for deployemnt (name and image to use)
  - rest defaults

- replicaset
  - another abstraction of layer
  - manages the replicas of a pod

```sh
k create deployment nginx-depl --image=nginx:alpine
k get replicaset
```


- Layers of Abstraction
  - Deployment : manages a replicaset
  - ReplicaSet : manages replicas of pods
  - Pod : is an abstraction of containers
  - Container

```sh
# edit deployement, but not pod directly
k edit deployment nginx-depl
```


- YAML configuration file
  - Attributes of `spec` are specific to the `kind`
  - each configuration file has 3 parts
    - metadata
    - specification
    - status: automatically generated by k8s (desired ==? actual) self-healing feature
      - k8s gets this status from `etcd`!
  - Store the YAML config file with your code (git repository)
  - `template` also has its own `metadata` and `spec`: applies to Pod
    - blueprint for a Pod


- Connecting the component
  - labels & selectors
  - `metadata` contains labels, `spec` contains selectors
    - metadata define key-value pair for label which is matched by the spec selector for pod
    - pod gets the label through the spec.template blueprint
    - pod belongs to deployment by label
    - deployment labels are connected to service's spec.selector
    - service's spec.selector uses deployment's metadata labels to make connection to deployement(pods)
  - service expose port (accessible) → forward to service targetPort → deployment's containerPort

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fe-nginx-deployment
  # NOTE label for deployment which is used by service to make connection to deployement(pods)
  labels:
    app: fe-nginx
spec:
  replicas: 2
  selector:
    # NOTE allows `Deployment` to find and manage Pods with this matching label
    matchLabels:
      app: fe-nginx
  template:
    metadata:
      # NOTE sets the labels for the `Pods` created by the Deployment.
      labels:
        app: fe-nginx
    spec:
      containers:
      - name: fe-nginx
        image: jnuho/fe-nginx:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
      #imagePullSecrets:
      #- name: regcred
```


```sh
k describe svc serivceName
  Endpoints: podip:targetPort
  : this Endpoint ip matches pod ip

k get pod podName -o wide
k get deploy nginx-depl -o yaml
  check the status is automatically generated by k8s
  retrieve result of status from etcd
```

- Complete Application setup with Kubernetes components
  - mongodb(internal service; no external requests), mongo-express(Web-app)
  - mongo express get url,id, pw from configmap and secret to connect to mongodb
  - mongo express accessible from browser: NodeIp:PortOfExternalService
  - 2 Deployment / Pod
  - 2 Service
  - 1 ConfigMap
  - 1 Secret
  - Browser → mongo express external service → mongoexpress pod → mongodb internal service → mongodb pod


- Namespace
  - kube-system: system processes, master and kubectl processes
  - kube-public: publicly accessible data, configmap, that contains cluster information `k cluster-info`
  - kube-node-lease: heartbeats of node, determines the availability of a node
  - default: resources you create

```sh
kubectl create namespace myNameSpace
```

- Group applications into namespaces
  - e.g. database/ logging / monitoring/ nginx-ingress/elastic stack
  - no need to create namespaces for smaller projects with about 10 users
  - create namespaces if there are many teams, same application(same name)
  - staging/development namespace resources use same resource in certain namespaces
  - blue/green deployment using namespaces (Production green/blue)
  - access and resource limits on nameaspaces


- Each NS must define own ConfigMap/Secret
  - suppose projectA, projectB namespaces
  - both namespace must have ConfigMap with exact same content

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-configmap
data:
  db_url: mysql-service.database
```

- Components, which can't be created within a namespace
  - persistent volume
  - node

```sh
k api-resources --namespaced=false
k api-resources --namespaced=true
```


- You can change the active namespace with kubens
  - without a need to `k get pod -n myNameSpace`

```sh
brew install kubectx
kubens
kubens my-namespace
  Active namespace is "my-namespace"
```



- Helm explained
  - package manage (e.g. apt)


- Helm for Elastic Search Stack for Logging
- requirement: yamls for
  - Stateful Set
  - ConfigMap
  - Secret
  - K8s User with permissions
  - Services
- First, helm provide packages for those to be used by anyone
  - install bundle of yamls
  - create your own helm charts with helm
  - push them to helm repository
  - download and use existing ones
  - e.g. database apps, monitoring apps(prometheus)
  - sharing helm charts is available
  - you can download reuse that configuration
  - `helm search <keyward>`
  - public/private helm registries
- Second, helm as a templating engine
  - for CI/CD: in your build, you can replace the values on the fly
  - Define a template with common attributes for many configurations
    - a common blueprint defined as a template YAML config
    - dynamic values are replaced by placeholders; `values.yaml`
      - values injection into template files
  - Same applications across different environments


- Helm chart structure

```
tree

mychart/        # name of the chart
  Chart.yaml    # meta info about chart: name,version,dependencies
  values.yaml   # values for the template files(can be overridden)
  charts/       # chart dependencies
  templates/    # template files
  READEME.md
  LICENSE

helm install <chartname>

# override values.yaml default values by:
# values.yaml + my-value.yaml => result
helm install --values=my-values.yaml <chartname>
helm install --set version=2.0.0

# BETTER TO HAVE my-values.yaml and values.yaml instead of `set`
```

- helm release management

- version2 vs. version3
- version2:
  - client  (cli)
  - server (tiller)
  - helm install(cli) → tiller execute yaml and deploy the cluster
  - helm install/upgrade/rollback → tiller create history with revision
    - revision 1,2... history is stored
    - downsides: tiller has too much power inside of k8s cluster
      - security risk
- version3: removed tiller for such security risk


- Volumes
  - Persistent Volume
  - Persistent Volume Claim
  - Storage class

- need for volumes
  - k8s no data persistence out of the box!
  - requires storage that doesn't depend on the pod lifecycle
  - storage must be available on all nodes
  - need to survive even if node/cluster crushes; highly available
    - outside of cluster?
  - writes/reads to directory

- Persistent volume
  - cluster resources used to storage data
  - defined by YAML
  - `spec`: how much storage
  - need actual physical sotrage:
  - persistent volume does not care about your actual storage
    - `pv` simply provides interface to the actual storage
    - it's like an external plugin to your cluster
  - could be hybrid: multiple storage types
    - one application uses local disk/nfs server/cloud stroages, etc.
  - in YAML for `pv`, specify in `spec`, which physical storage to use

- Check types of vlumes in k8s document

- gcp cloud storage

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-volume
  failure-domain.beta.kubernetes.io/zone: us-central1-a__us-central1-b
spec:
  capacity:
    storage: 400Gi
  accessModes:
  - ReadWriteOnce
  gcePersistentDisk:
    pdName: my-data-disk
    fsType: ext4
```

- local storage

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  capacity:
    storage: 100Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /mnt/disks.ssd1
  modeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - example-node
```

- Persistent Volumes are NOT namespaced
  - PV outside of the namesapces
  - accessible to the whole cluster

- Local vs. Remote volume types
  - each volume type has it's own use case!
  - local volume types violoate 2. and 3. requirement for data persistence:
    - (X) Being tied to 1 specific node
    - (X) Surviving cluster crashes
- For DB persistence, almost always use REMOTE STORAGE!!!



- StatefulSet
  - What is it and why it is used?
  - how `StatefulSet` differs from `Deployment`?
  - specifically for stateful appliations!
    - e.g. stateful apps: database apps
    - e.g. stateless apps: don't keep record of state, each request is completely new


- Stateful and stateless applications example
  - nodejs(stateless) + mongodb(stateful)
  - http request (doesn't depend on previous data to handle)→ nodejs
    - handle it based on the payload of request
    - update/query from mongodb app
  - mongodb update data based on previous state / query data
    - depends on most up-to-date data/state

- Stateless apps are deployed using `Deployment` component
- Stateful apps are deployed using `StatefulSet` component
- Both `Deployment` and `StatefulSet` manage pods based on container specification!



- K8s Services
  - ClusterIP
  - NodePort
  - LoadBalancer
  - Headless

- each pod has its own ip address
- pods are ephermeral - are descroyed frequently!
- service provides stable ip address.
- service does load balancing into pods
- loose coupling 
- within & outside cluster


- ClusterIP Services
  - default type
  - e.g. microservices app deployed
    - in pod : app container(3000)+sidecar container (9000: collects logs)
    - pod assgiend in node ip range: 10.2.2.5 (started on node2)
    - where node1: 10.2.1.x
    - where node2: 10.2.2.x
    - where node3: 10.2.3.x
    - `k get pod -o wide` to check pod ip
    - Ingress → Service(ClusterIP) → Pods
    - Sevice's `spec.selector` : which Pods it forward to
    - Sevice's `spec.ports.targetPort` : which Ports it forward to
    - Pods are identified via selectors
      - key value pairs for selctor
      - Pod: `spec.template.metadata.labels`
      - Service: `spec.selector`
        - service forwards request to matching Pods
    - Service Endpoint is CREATED with the same name as Service
    - keeps track of which Pods are the members/endppoints of the Service
    - each time pods recreated, Endpoints are also updated to track that
    - Service `spec.ports.port`: can be arbitrary
    - Service `spec.ports.targetPort`: MUST MATCH deployment's Pod `containerPort`
    - Multi-port services (two container specified in deployment.yaml)
      - mongo-db application 27017
      - mongo-db exporter (Prometheus) 9216
        - Prometheus scapes data from mododb-exporter via port 9216
    - service have to handle two requests via two ports 27017, 9216

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: microservice-one
spec:
  replicas: 2
  # ...
  template:
    metadata:
      labels:
        app: microservice-one
    spec:
      containers:
      - name: ms-one
        image: my-private-repo/ms-one:latest
        ports:
        - containerPort: 3000
      - name: log-collector
        image: my-private-repo/log-collector:latest
        ports:
        - containerPort: 9000
```

- Multi-port service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
spec:
  selector:
    app: mongodb
  ports:
    - name: mongodb
      protocol: TCP
      port: 27017
      targetPort: 27017
    - name: mongodb-exporter
      protocol: TCP
      port: 9216
      targetPort: 9216
```



- Headless Service
  - Client wants to communicate with 1 specific Pod directly
  - Pods want to talk directly with specific Pod
  - So, not randomly selected (no Load balancing)
  - Use case: `Stateful` applications
    - such as databases(mysql,mongodb, elasticsearch)
    - Pods replicas are not identical
    - Only Master Pod is allowed to write to DB (write/read)
    - Worker Pods are for only (read)
    - Worker Pods must connect to Master Pod to sync their data after Master Pods made changes to the data
    - When a Worker Pod is created, it must clone the most recent Worker Pod
  - Client need to figure out IP addresses of each Pod
    - Option 1: API call to k8s API Server?
      - list of pods and ip addresses
      - too tied to k8s api and inefficient
    - Option 2: DNS lookup
      - k8s allows client to discover Pod ip addresses
      - DNS lookup for service - returns single IP address which belongs to a Service (ClusterIP address)
    - BUT setting `sepc.cluseterIP` to `None` returns Pod IP address instead!!!

- Define headless Service:
  - NO CLUSTER IP address is assigned!!!

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service-headless
spec:
  clusterIP: None
  selector:
    app: mongodb
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```

- Two services exist alongside each other
  - `mongodb-service`
  - `mongodb-service-headless`

- Use headles service when client needs to perform write into mongodb Master Pod or for Pods to talk to each other for data synchronization

```sh
k get svc

NAME                     TYPE       CLUSTER-IP EXTERNAL-IP PORT(S)
mongodb-service-headless ClusterIP  None       <none>      27017/TCP
```

- 3 Service `type`
  - ClusterIP: default, internal service, only accessible within cluster
    - no external traffic can directly address the ClusterIP service
  - NodePort: accessible on a static port on each worker node in cluster
    - External traffic has access to fixed port on each Worker Node
    - `nodePort` range should be: 30000 - 32767
    - `http://ip-address-worker-node:nodePort`
    - When you create NodePort Service, ClusterIP Service is also automatically created because nodePort has to be routed to `port` of Service
      - `nodePort` → `port`
      - e.g.  `port:3200`, `nodePort:30008`
        - cluster-ip:3200
        - node-ip:30008
  - LoadBalancer
    - LoadBalancer(Cloud providers')
    - AWS, GCP, AZURE
    - When Service of type LoadBalancer is created,
      - NodePort and ClusterIP Service are created automatically!
      - nodeport is not accessible directly from external browser
        - instead via LoadBalancer!!!

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ms-service-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: microservice-one
  ports:
    - protocol: TCP
      port: 3200
      targetPort: 3000
      # only via LoadBalancer though!
      nodePort: 30010
```


- LoadBalancer > NodePort > ClusterIP
  - LoadBalancer Service is an extension of NodePort Service
  - NodePort Service is an extension of ClusterIP Service


- Wrap-up
  - NodePort Service NOT for external connection! TEST-ONLY
  - two common practice:
    - Ingress → Service (ClusterIP)
    - LoadBalanceri → Service (ClusterIP)



### Kubernetes Networking

- [Medium Post](https://medium.com/google-cloud/understanding-kubernetes-networking-pods-7117dd28727)
  - [Networking terminology](https://www.digitalocean.com/community/tutorials/an-introduction-to-networking-terminology-interfaces-and-protocols)
  - [Networking - IP, Subnets, CIDR](https://www.digitalocean.com/community/tutorials/understanding-ip-addresses-subnets-and-cidr-notation-for-networking)






- Kubernetes
  - 컨테이너 오케스트레이션 플랫폼으로 컨테이너 어플리케이션 deploy, manage, scaling 프로세스 자동화
  - Kubernetes clusters : 리눅스 컨테이너 호스트를 cluster로 그룹화하고 관리
    - on-premise, public/private/hybrid clouds에 적용가능
    - 바른 스케일링이 필요한 cloud-native 어플리케이션에 적합한 플랫폼
  - 클라우드 앱 개발시 optimization에 유용
  - physical 또는 VM 클러스터에 컨테이너들을 scheduling 하고 run 할 수 있음
  - 클라우드 네이티브 앱을 '쿠버네티스 패턴'을 이용하여 쿠버네티스를 런타임 플랫폼으로 사용하여 만들수 있음
  - 추가 기능으로:
    - 여러호스트에 걸쳐서 컨테이너를 Orchestrate 할 수 있음
    - 엔터프라이즈 앱실행을 위해 리소스를 최대화하여 하드웨어 운용 가능
    - 어플리케이션 배포와 업데이트를 제어 및 자동화
    - Stateful 앱을 실행 하기 위해 스토리지를 마운트 하고 추가 가능
    - 컨테이너 애플리케이션과 리소스를 scaling 할 수 있음
  - 쿠버네티스는 다른 프로젝트들과 결합하여 효율적인 사용
    - Registry: Docker Registry
    - Networking
    - Telemetry
    - Security: LDAP, SELinux,RBAC, OAUTH with multitenancy layers
    - Automation
    - Services

- Kubernetes Architecture
  - [image1](https://devopscube.com/wp-content/uploads/2022/12/k8s-architecture.drawio-1.png)
  - [image2](https://www.redhat.com/rhdc/managed-files/kubernetes_diagram-v3-770x717_0_0_v2.svg)

- TERMS
  - Control Plane
    - 쿠버네티스 노드들을 컨트롤하는 프로세스의 집합
    - 여기서 모든 Task 할당이 이루어 짐
  - Node : 컨트롤 Plane으로 부터 할당된 Task를 수행하는 머신
  - Pod: 1개의 Node에 Deploy된 한개 이상의 컨테이너들
    - 파드에 있는 컨테이너들은 IP 주소, IPC (inter-process-communication), Hostname, 리소스
  - Replication 컨트롤러 : 몇개의 동일 pod 카피들이 클러스터에서 실행되어야 하는지 컨트롤
  - Service : Pods로부터 work definition을 분리함.
    - Kubernetes Service Proxy들이 자동으로 서비스 리퀘스트를 pod에 연결함
    - Cluster 내에서 어디로 움직이든 또는 replace 되더라도 자동으로 연결 됨.
  - Kubelet : 이 서비스는 노드에서 실행되며, 컨테이너 manifest를 읽고, 정의된 컨테이너들이 시작되고 작동하도록 함

- 동작원리
  - 클러스터 : 동작 중인 쿠버네티스 deployment를 클러스터라고 합니다.
    - 클러스터는 컨트롤 plane과 compute 머신(노드) 두가지 파트로 나눌 수 있습니다.
      - Control Plane + Worker nodes
    - 각각의 노드는 리눅스환경으로 볼 수 있으며, physical/virtual 머신입니다.
    - 각각의 노드는 컨테이너들로 구성된 pod들을 실행합니다.
    - 컨트롤러 플레인은 클러스터의 상태를 관리
      - 어떤 어플리케이션이 실행되고 있는지, 어떤 컨테이너 이미지가 사용 되고 있는지 등
      - Compute 머신은 실제로 어플리케이션과 워크로드들을 실행 합니다.
  - 쿠버네티스는 OS위에서 동작하면서 노드들위에 실행 중인 컨테이너 pod들과 interact 합니다.
    - 컨트롤러플레인은 admin으로부터 커멘드를 받아, Compute머신에 해당 커멘드들을 적용합니다.


- Youtube Tutorial (TechWorld with Nana)

```
- Deployment > ReplicaSet > Pod > Container
  - use kubectl command to manage deployment

```sh
k get pod

k get services

k create deployment nginx-depl --image=nginx
k get deployment
k get pod
k get replicaset

k edit deployement nginx-depl
k get pod
  NAME                          READY   STATUS    RESTARTS   AGE
  nginx-depl-8475696677-c4p24   1/1     Running   0          3m33s
  mongo-depl-5ccf565747-xtp89   1/1     Running   0          2m10s

k logs nginx-depl-56cb8b6d7-6z9w6

k exec -it [pod name] -- bin/bash

k exec -it mongo-depl-5ccf565747-xtp89 -- bin/bash
k delete deployment mongo-depl
```


- microk8s 환경
  - https://microk8s.io/docs/getting-started
  - https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s?&_ga=2.260194125.1119864663.1678939258-1273102176.1678684219#1-overview


```sh
sudo snap install microk8s --classic

# 방화벽설정
# https://webdir.tistory.com/206

sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
su - $USER
microk8s status --wait-ready

vim .bashrc
  alias k='microk8s kubectl'
  alias helm='microk8s helm'

source .bashrc
```

- Microk8s, Ingress, metallb, nginx controller로 외부 서비스 만들기
  - 참고 문서
    - https://kubernetes.github.io/ingress-nginx/deploy/baremetal/
    - https://benbrougher.tech/posts/microk8s-ingress/
    - https://betterprogramming.pub/how-to-expose-your-services-with-kubernetes-ingress-7f34eb6c9b5a

- Ingress는 쿠버네티스가 외부로 부터 트래픽을 받아서 내부 서비스로 route할 수 있도록 해줌
  - 호스트를 정의하고, 호스트내에서 sub-route를 통해
  - 같은 호스트네임의 다른 서비스들로 route할 수 있도록 함
  - Ingress rule을 통해 하나의 Ip 주소로 들어오도록 설정
  - Ingress Controller가 실제 traffic route하며, Ingress는 rule을 정의하는 역할

- 이미지 만들기 → Dockerhub에 push

```sh
# 이미지 만들기
cd learn/yaml/helloworld/docker
docker build -t server-1:latest -f build/Dockerfile .
docker tag server-1 jnuho/server-1
docker push jnuho/server-1
```

- simple-service.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hellok8s-deployment
  labels:
    app: hellok8s
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hellok8s
  template:
    metadata:
      labels:
        app: hellok8s
    spec:
      containers:
      - name: hellok8s
        image: jnuho/server-1
        ports:
        - containerPort: 8081
---
apiVersion: v1
kind: Service
metadata:
  name: hellok8s-service
  # Use specific ip for metallb
  annotations:
    metallb.universe.tf/loadBalancerIPs: 172.16.6.100
spec:
  type: LoadBalancer
  selector:
    app: hellok8s
  ports:
  - port: 8081
    targetPort: 8081
```

```sh
k apply -f simple-service.yaml
k get svc
  NAME               TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)          AGE
  kubernetes         ClusterIP      10.152.183.1    <none>         443/TCP          5d19h
  hellok8s-service   LoadBalancer   10.152.183.58   <none>         8081:31806/TCP   114s
```

```sh
# 사용중 ip인지 확인하기: 100-105
ping 172.16.6.100

microk8s enable metallb:172.16.6.100-172.16.6.105

# 로드밸런서 서비스의 IP가 metallb에 의해 할당됨
# 172.16.6.100:8081로 애플리케이션 접근

k get svc
  NAME               TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)          AGE
  kubernetes         ClusterIP      10.152.183.1    <none>         443/TCP          5d19h
  hellok8s-service   LoadBalancer   10.152.183.58   172.16.6.100   8081:31806/TCP   114s

# 브라우저로 애플리케이션 접근 172.16.6.100:8081
curl 172.16.6.100:8081
```

