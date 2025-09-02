# RDS subnet group
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-wp-subnet-group"
  subnet_ids = [aws_subnet.private1.id, aws_subnet.private2.id]
}

# RDS INSTANCE
resource "aws_db_instance" "wordpress" {
  identifier = var.rds_identifier

  engine         = "mysql"
  engine_version = "8.0"

  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_user_name
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]

  # security / maintenance
  publicly_accessible = false
  deletion_protection = false

  # snapshots: DO NOT set final_snapshot_identifier when skip_final_snapshot=true
  skip_final_snapshot = true

  tags = {
    Name = "RDS Instance"
    App  = "wordpress"
    # Env  = var.env
  }
}

# RDS security group
resource "aws_security_group" "rds_security_group" {
  name        = "rds-wp-security-group"
  description = "Security group for RDS instance"
  vpc_id      = aws_vpc.this.id

  ingress {
    description     = "MySQL from web SG"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.allow_ssh.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "RDS Security Group" }
}
