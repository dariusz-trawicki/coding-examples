provider "vault" {
  address = "http://127.0.0.1:8200"

  auth_login {
    path = "auth/approle/login"
    parameters = {
      role_id   = var.vault_role_id
      secret_id = var.vault_secret_id
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}