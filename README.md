# Real-Time Customer Feedback Analytics Dashboard

This is a Python-based feedback analytics application that allows concurrent sentiment and topic analysis of feedbacks received from various source platforms. After processing, the aggregated results are displayed on a dashboard for easy visualization and interpretation.

## Demo
For demo purposes, the dashboard allows sending of sample requests, as well as checking status of requests using their task ID.

## Setup
### Prerequisites
- minikube
- kubectl

### Command
The `manifest.yaml` file contains the Kubernetes manifest for the application. To deploy the application, run the following command:
```bash
eval $(minikube -p minikube docker-env) # Connect to minikube's docker daemon
docker build -t myimage .
kubectl apply -f manifest.yaml
```
 
## Usage
### Forwarding miniKube's port
To access the dashboard, you will need to forward the port of the dashboard service from minikube to your local machine. To do so, run the following command:
```bash
minikube service fastapi-svc --url  # Needed only if desired to access the FastAPI deployment directly
minikube service streamlit-svc --url
```

## Configuration
The workers can be scaled independently by changing the `replicas` field of `tasktiger-worker` in the `manifest.yaml` file. The default value is 1.

### Architecture
Streamlit --> FastAPI --> Redis <-- TaskTiger workers
