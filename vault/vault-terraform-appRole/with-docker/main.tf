data "vault_kv_secret_v2" "db_config" {
  mount = "secret"
  name  = "my-app/config"
}

output "db_username" {
  value     = data.vault_kv_secret_v2.db_config.data["db_username"]
  sensitive = true
}

output "db_password" {
  value     = data.vault_kv_secret_v2.db_config.data["db_password"]
  sensitive = true
}

output "env_file" {
  value = <<EOT
DB_USERNAME=${data.vault_kv_secret_v2.db_config.data["db_username"]}
DB_PASSWORD=${data.vault_kv_secret_v2.db_config.data["db_password"]}
EOT

  sensitive = true
}
