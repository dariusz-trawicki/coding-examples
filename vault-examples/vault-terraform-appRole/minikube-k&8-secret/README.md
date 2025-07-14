# Kubernetes (minikube): create Secret z danych Vaulta

### Minikube

```bash
# Run Kubernetes cluster
minikube start
# Test
kubectl get pods -A
```

### Vault: config AppRole

```bash
export VAULT_ADDR='http://127.0.0.1:8200'

vault auth enable approle

vault write auth/approle/role/terraform-role \
  token_policies="default" \
  token_ttl=60m \
  token_max_ttl=120m

vault read auth/approle/role/terraform-role/role-id
vault write -f auth/approle/role/terraform-role/secret-id

# *** output ***
# Success! Enabled approle auth method at: approle/
# Success! Data written to: auth/approle/role/terraform-role
# Key        Value
# ---        -----
# role_id    be4d773b-cdab-bcc9-6a6e-fe2b014e47db
# Key                   Value
# ---                   -----
# secret_id             fce632f8-f838-05b2-52ca-f50bf875xxxx
# secret_id_accessor    2d3618cf-e847-ad4b-3532-30985697xxxx
# secret_id_num_uses    0
# secret_id_ttl         0s

# Save role_id i secret_id.
```

### Create secret example in Vault

```bash
vault kv put secret/my-app/config db_username="admin" db_password="secret123"
# *** output ***
# ====== Secret Path ======
# secret/data/my-app/config

# ======= Metadata =======
# Key                Value
# ---                -----
# created_time       2025-07-12T10:46:41.546584Z
# custom_metadata    <nil>
# deletion_time      n/a
# destroyed          false
# version   

# Test
vault kv get secret/my-app/config
# *** output ***
# ====== Secret Path ======
# secret/data/my-app/config

# ======= Metadata =======
# Key                Value
# ---                -----
# created_time       2025-07-12T11:03:24.119242Z
# custom_metadata    <nil>
# deletion_time      n/a
# destroyed          false
# version            2

# ======= Data =======
# Key            Value
# ---            -----
# db_password    secret123
# db_username    admin
```

### Load the policy into Vault (granting permissions to create child tokens)

```bash
vault policy write terraform-policy terraform-policy.hcl
# *** output ***
# Success! Uploaded policy: terraform-policy
# Test
vault write auth/approle/role/terraform-role token_policies="terraform-policy"
# *** output ***
# Success! Data written to: auth/approle/role/terraform-role
vault read auth/approle/role/terraform-role
```

### Terraform:

In `terraform.tfvars`, set the following variables:

```hcl
vault_role_id   = "be4d773b-cdab-bcc9-6a6e-fe2b014exxxx"
vault_secret_id = "fce632f8-f838-05b2-52ca-f50bf875xxxx"
```

```bash
terraform init
terraform plan
terraform apply
# *** output ***
# Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

# The my-app-secret secret has been created in the Kubernetes cluster (Minikube), in the default namespace.

# Test
kubectl get secret my-app-secret -o yaml
# *** output ***
# apiVersion: v1
# data:
#   DB_PASSWORD: c2VjcmV0MTIz            # Data encoded (by terraform) in Base64
#   DB_USERNAME: YWRtaW4=
# kind: Secret
# metadata:
#   creationTimestamp: "2025-07-12T11:57:31Z"
#   name: my-app-secret
#   namespace: default
#   resourceVersion: "242647"
#   uid: 76746228-361b-4816-b000-6373723cc840
# type: Opaque


# Apply example deployment
kubectl apply -f deployment.yaml
# *** output ***
# deployment.apps/my-app created

# Test:
kubectl get pods
# *** output ***
# NAME                      READY   STATUS      RESTARTS   AGE
# my-app-7f67fb669b-l2wp6   1/1     Running     0          82s
kubectl exec -it my-app-7f67fb669b-l2wp6 -- printenv | grep DB_
# *** output ***
# DB_USERNAME=admin
# DB_PASSWORD=secret123
```