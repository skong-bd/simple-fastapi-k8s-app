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
