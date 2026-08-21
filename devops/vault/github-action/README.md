# Github action and Vault example

## Install ACT (local runner GitHub Actions)

```bash
brew install act
```

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

git init
git add .
git commit -m "init for act test"

killall vault   # if needed
vault server -dev
# **output ***
# Root Token: hvs.zg4ybNWejyGEt2afe5RSxxxx

export VAULT_ADDR='http://host.docker.internal:8200'
export VAULT_TOKEN='hvs.zg4ybNWejyGEt2afe5RSxxxx'

# write/add a secret to Vault
vault kv put secret/ci/app API_KEY=local-12345
```

In `local-vault-ci.yml` file set:

```yml
    env:
      VAULT_ADDR: http://host.docker.internal:8200
      VAULT_TOKEN: hvs.zg4ybNWejyGEt2afe5RSxxxx
```

Run

```bash
act -j local-test --container-architecture linux/amd64
# if needed - choose: Medium
# *** output ***
# API_KEY from Vault: local-12345
# | .env file created:
# | API_KEY=local-12345
```

