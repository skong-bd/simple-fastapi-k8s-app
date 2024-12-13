# Simple FastAPI App with Kubernetes Cluster Setup

## Pre-requisites
- `kubectl` CLI (`brew install kubectl`)
- `minikube` CLI (`brew install minikube`)
- `poetry` CLI (`pip install poetry`)
- `helm` CLI (`brew install helm`)

## Build and Push Docker Image
``` bash
docker build -t <IMAGE_NAME:IMAGE_TAG> -f dockerfile .
docker push <IMAGE_NAME:IMAGE_TAG>
```

## Start Kubernetes Cluster, Run Pods and Services
``` bash
# Create and Start a New Kubernetes Cluster
minikube start

# Deploy Pods and Services in the Kubernetes Cluster
kubectl apply -f ./kubernetes/deployment.yaml
```

## Verify all Pods are Created and Running
``` bash
kubectl get pods

# NAME                                  READY   STATUS    RESTARTS   AGE
# simple-fastapi-app-585b84f5d4-9mf48   1/1     Running   0          117m
# simple-fastapi-app-585b84f5d4-c8vbh   1/1     Running   0          117m
# simple-fastapi-app-585b84f5d4-gcdp8   1/1     Running   0          117m
```

## Verify all Services are Created and Running
``` bash
kubectl get services

# NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# kubernetes           ClusterIP   10.96.0.1       <none>        443/TCP    119m
# simple-fastapi-app   ClusterIP   10.106.18.109   <none>        8000/TCP   116m
```

## Setup Nginx Ingress Controller
``` bash
# install custom resource definitions (CRD) 
kubectl apply -f https://raw.githubusercontent.com/nginxinc/kubernetes-ingress/v3.7.2/deploy/crds.yaml

# install nginx-ingress controller via helm charts
helm install nginx-ingress oci://ghcr.io/nginxinc/charts/nginx-ingress --version 1.4.2
```





## Create Secrets, Nginx Policy and Virtual Server
``` bash
# multiple api keys can be put into a single Secret Resource
kubectl apply -f nginx/secret.yaml

# one policy resource can only have one policy spec
# e.g. rate limiting and api key auth are two different policy specs and they have to be created separately in two different policy resources
kubectl apply -f nginx/policy.yaml

# virtual server (and routes) can apply one or more policy
kubectl apply -f nginx/virtual-server.yaml
```

## Test the FastAPI
``` bash
# Enable Minikube Tunneling on one Terminal (sudo mode is required, provide you windows/mac password)
minikube tunnel

# Open another Terminal and use `curl` to perform the API Testing
curl localhost -H "apikey:aaabbbccc"  # this should work
curl localhost -H "apikey:xxxyyyzzz"  # this should work
curl localhost -H "apikey:abcabcabc"  # this shouldn't work
```

## References
- https://docs.nginx.com/nginx-ingress-controller/installation/installing-nic/installation-with-helm/
- https://docs.nginx.com/nginx-ingress-controller/configuration/policy-resource/
- https://docs.nginx.com/nginx-ingress-controller/configuration/virtualserver-and-virtualserverroute-resources/