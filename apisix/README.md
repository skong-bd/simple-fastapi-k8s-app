# Simple FastAPI App with Kubernetes Cluster Setup

## Pre-requisites
- `kubectl` CLI (`brew install kubectl`)
- `minikube` CLI (`brew install minikube`)
- `poetry` CLI (`pip install poetry`)

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

## Setup Apisix using Helm
``` bash
helm repo add apisix https://charts.apiseven.com
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install apisix apisix/apisix \
  --set service.type=NodePort \
  --set ingress-controller.enabled=true \
  --create-namespace \
  --namespace ingress-apisix \
  --set ingress-controller.config.apisix.serviceNamespace=ingress-apisix \
  --set ingress-controller.config.apisix.adminAPIVersion=v3
kubectl get service --namespace ingress-apisix
```

## Create Secrets, Apisix Consumer and Apisix Routes
``` bash
# Deploy Pods and Services in the Kubernetes Cluster
kubectl apply -f ./apisix/config.yaml

# Verify Secrets are created
kubectl get secrets
```

## Test the FastAPI
``` bash
# Get Minikube Service URL for apisix-gateway on one Terminal
minikube service apisix-gateway --url -n ingress-apisix

# Take note of the port returned from the execution above. e.g. http://127.0.0.1:64412
# Open another Terminal and use `curl` to perform the API Testing
curl localhost:{PORT} -H "apikey:aaabbbccc"  # this should work
curl localhost:{PORT} -H "apikey:xxxyyyzzz"  # this should work
curl localhost:{PORT} -H "apikey:abcabcabc"  # this shouldn't work
``` 

## References
- https://apisix.apache.org/docs/ingress-controller/deployments/minikube/
- https://apisix.apache.org/docs/ingress-controller/tutorials/enable-authentication-and-restriction/#how-to-enable-authentication
