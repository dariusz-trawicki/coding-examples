
### Demo: installing `MLflow` on `Minikube`

- `backend database`: `Postgres` (for parameters, metrics etc.)
- `artifact store`  : `MinIO` (for models, files etc.)

```bash
minikube start
kubectl config use-context minikube

kubectl apply -f k8s-mlflow.yaml

# Tests:
kubectl -n mlflow get pods
# Output example:
# NAME                        READY   STATUS      RESTARTS   AGE
# minio-5945c96888-n56ss      1/1     Running     0          8m3s
# minio-setup-spkzx           0/1     Completed   0          4m17s
# mlflow-6f986b8878-5hkqk     1/1     Running     0          8m3s
# postgres-8595f98648-vbdpq   1/1     Running     0          8m3s
```

```bash
# terminal I:
# MLflow UI/API → http://127.0.0.1:5000
kubectl -n mlflow port-forward svc/mlflow 5000:5000

# terminal II
# MinIO Console → http://127.0.0.1:9001
kubectl -n mlflow port-forward svc/minio 9001:9001

# terminal III:
curl -I http://127.0.0.1:5000/
```

#### Run demo projects

```bash
conda create -n mlflow_env python=3.12
conda activate mlflow_env

# Test
conda env list

pip install -r requirements.txt

# terminal IV
jupyter lab

# Note: Run the notebooks in the following order:
# - 01_first_experiment.ipynb
# - 02_ml_flow_binary_classification.ipynb
# - 03_ml_flow_model_management.ipynb
```

#### CLEAN UP

```bash
conda deactivate 
conda env remove -n mlflow_env

kubectl delete -f k8s-mlflow.yaml
kubectl delete namespace mlflow

minikube delete
```