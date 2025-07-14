# Retrieve the secret from Vault (KV version 2)
data "vault_kv_secret_v2" "db_config" {
  mount = "secret"
  name  = "my-app/config"
}

# Create a Kubernetes Secret from the Vault data
resource "kubernetes_secret" "db_secret" {
  metadata {
    name      = "my-app-secret"
    namespace = "default"
  }

  data = {
    DB_USERNAME = data.vault_kv_secret_v2.db_config.data["db_username"]
    DB_PASSWORD = data.vault_kv_secret_v2.db_config.data["db_password"]
  }


  type = "Opaque"
}
