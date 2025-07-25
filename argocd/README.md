# ArgoCD Installation in Minikube with Git-Backed Application State

```bash
# Install ArgoCD CLI
brew install argocd

minikube start
minikube status


kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Test
kubectl get pods -n argocd
# wait ...
# *** output ***
# NAME                                                READY   STATUS    RESTARTS       AGE
# argocd-application-controller-0                     1/1     Running   0              3m31s
# argocd-applicationset-controller-655cc58ff8-8x9hj   1/1     Running   0              3m31s
# argocd-dex-server-7d9dfb4fb8-9xf4w                  1/1     Running   1 (3m1s ago)   3m31s
# argocd-notifications-controller-6c6848bc4c-hqgm9    1/1     Running   0              3m31s
# argocd-redis-656c79549c-thslw                       1/1     Running   0              3m31s
# argocd-repo-server-856b768fd9-nwxvl                 1/1     Running   0              3m31s
# argocd-server-99c485944-f55kg                       1/1     Running   0              3m31s


# Forward port to UI ArgoCD (8080)
kubectl port-forward svc/argocd-server -n argocd 8080:443


# Get the default Argo CD "admin" password stored in a Kubernetes secret:

kubectl -n argocd get secret argocd-initial-admin-secret -n argocd -o yaml
# apiVersion: v1
# data:
#   password: QkwtWjhhTzVaVEFadlNRNQ==
# kind: Secret
# metadata:
#   creationTimestamp: "2025-07-14T13:34:24Z"
#   name: argocd-initial-admin-secret
#   namespace: argocd
#   resourceVersion: "249965"
#   uid: ca4f2df7-0510-4c42-8a65-f9a9a1a5a9da
# type: Opaque

# decode password
echo QkwtWjhhTzVaVEFadlNRNQ==| base64 --decode
# *** output (example) ***
# BL-Z8aO5ZTAZvSQ5%   # ignore "%"

# OR faster:
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 --decode
echo
# *** output (example) ***
# BL-Z8aO5ZTAZvSQ5
```

### Login in:

1. CLI:

```bash
argocd login localhost:8080 --username admin --password BL-Z8aO5ZTAZvSQ5 --insecure
# *** output ***
# 'admin:login' logged in successfully
# Context 'localhost:8080' updated
```

2. In the browser (UI)

Open: http://localhost:8080, (username: `admin`, password: `BL-Z8aO5ZTAZvSQ5`).


### Deploy ArgoCD Application Configuration

```bash
kubectl apply -f application.yaml
# *** output ***
# application.argoproj.io/myapp-argo-application created

argocd app list
# *** output ***
# NAME                           CLUSTER                         NAMESPACE  PROJECT  STATUS  HEALTH   SYNCPOLICY  CONDITIONS  REPO                                                     PATH        TARGET
# argocd/myapp-argo-application  https://kubernetes.default.svc  myapp      default  Synced  Healthy  Auto-Prune  <none>      https://github.com/dariusz-trawicki/coding-examples.git  argocd/dev  HEAD
```

### View Deployed Application in ArgoCD

Open your browser and go to: http://localhost:8080
- In the `Applications panel`, click on the `myapp-argo-application` box
- Inside the application view, click on the `myapp-xxxxxxxxxxxxxxx` Pod

The container image listed as: `nginx:1.25`


## Run/Test – Apply Modifications

### Update the Deployment (NGINX Image Version) and Push Changes to Git

In the `dev/deployment.yaml` file, update the container image version:

Change:

```yaml
image: nginx:1.25
```

To:

```yaml
image: nginx:1.27
```

#### Commit and push the change:

```bash
git add .
git commit -m "Update NGINX image to version 1.27"
git push origin main
```

#### View Deployed Application in ArgoCD

Open your browser and go to: http://localhost:8080
- In the `Applications panel`, click on the `myapp-argo-application` box
- Click on the `REFRESH` button
- Inside the application view, click on the `myapp-xxxxxxxxxxxxxxx` Pod

The container image listed as: `nginx:1.27`
