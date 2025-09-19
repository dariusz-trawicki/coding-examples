#EC2
resource "aws_instance" "web" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.ssh_key.key_name
  vpc_security_group_ids      = [aws_security_group.allow_ssh.id]
  subnet_id                   = aws_subnet.public1.id
  availability_zone           = var.zone1
  associate_public_ip_address = true

  tags = {
    Name    = var.instance_name
    Project = var.project_name
  }

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    rds_host     = aws_db_instance.wordpress.address
    rds_user     = var.db_user_name
    rds_password = var.db_password
    rds_dbname   = var.db_name
    # DOCKER_COMPOSE_VERSION = "v2.24.6"
  })
}
