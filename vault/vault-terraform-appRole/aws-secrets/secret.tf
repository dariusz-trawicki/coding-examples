resource "aws_secretsmanager_secret" "db_secret" {
  name = "my-app-db-secret"
}

resource "aws_secretsmanager_secret_version" "db_secret_version" {
  secret_id = aws_secretsmanager_secret.db_secret.id
  secret_string = jsonencode({
    db_username = data.vault_kv_secret_v2.db_config.data["db_username"]
    db_password = data.vault_kv_secret_v2.db_config.data["db_password"]
  })
}
