# Docker: passing data from Vault as environment variables

## Vault: config AppRole

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
# role_id    be4d773b-cdab-bcc9-6a6e-fe2b014exxxx
# Key                   Value
# ---                   -----
# secret_id             fce632f8-f838-05b2-52ca-f50bf875xxxx
# secret_id_accessor    2d3618cf-e847-ad4b-3532-30985697xxxx
# secret_id_num_uses    0
# secret_id_ttl         0s

# Save role_id i secret_id.
```

## Create secret example in Vault

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
```

Upload the policy to Vault (granting permissions to create child tokens)

```bash
vault policy write terraform-policy terraform-policy.hcl
# *** output ***
# Success! Uploaded policy: terraform-policy
# test
vault write auth/approle/role/terraform-role token_policies="terraform-policy"
# *** output ***
# Success! Data written to: auth/approle/role/terraform-role
vault read auth/approle/role/terraform-role

```

## Terraform

```bash
terraform init
terraform plan
terraform apply
```

## Example: Injecting into a Docker container using environment variables

```bash
terraform output -raw env_file > .env

# example image (node:18)
docker build -t my-app-image .
docker run --rm --env-file .env -p 3000:3000 my-app-image
#  *** output ***
# DB_USERNAME: admin
# DB_PASSWORD: secret123
# Open: http://localhost:3000
```