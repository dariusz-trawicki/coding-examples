# Vault (HashiCorp Vault)

## Install Vault

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/vault
vault --version
#  test
vault server -dev

# *** output ***
# WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
# and starts unsealed with a single unseal key. The root token is already
# authenticated to the CLI, so you can immediately begin using Vault.

# You may need to set the following environment variables:

#     $ export VAULT_ADDR='http://127.0.0.1:8200'

# The unseal key and root token are displayed below in case you want to
# seal/unseal the Vault or re-authenticate.

# Unseal Key: MKsb/R67R0/MBl3c+SvPKwPAxpeHa1QLHf2oVt6uxxx=
# Root Token: hvs.gkNI6GG4eXMlwqi9Uqk1xxxx

# Development mode should NOT be used in production installations!

# Open: http://127.0.0.1:8200
# Method: Token
# Token:  use Root Token: hvs.gkNI6GG4eXMlwqi9Uqk1xxxx
```