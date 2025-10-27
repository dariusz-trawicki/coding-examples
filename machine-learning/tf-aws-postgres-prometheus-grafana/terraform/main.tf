# Get the default (regional) Postgres engine version and its parameter group family
data "aws_rds_engine_version" "pg_default" {
  engine       = "postgres"
  default_only = true
}

resource "aws_db_instance" "rds" {
  engine              = "Postgres"
  identifier          = "${var.db_name}-instance"
  db_name             = var.db_name
  allocated_storage   = 20
  engine_version      = data.aws_rds_engine_version.pg_default.version
  instance_class      = "db.t3.micro"
  username            = var.db_user_name
  password            = var.user_password
  skip_final_snapshot = true
  publicly_accessible = true
}