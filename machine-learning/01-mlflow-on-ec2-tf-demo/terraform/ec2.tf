# --- Ubuntu AMI ---
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# --- EC2 + systemd service for MLflow ---
locals {
  user_data = <<-EOF
    #!/bin/bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    # Base packages
    apt-get update -y
    apt-get install -y python3-venv awscli

    # Create directory for the backend (sqlite) and MLflow metadata
    install -d -o ubuntu -g ubuntu /var/mlflow

    # Virtual environment for MLflow
    python3 -m venv /opt/mlflow/venv
    /opt/mlflow/venv/bin/pip install --upgrade pip
    /opt/mlflow/venv/bin/pip install "mlflow>=3.4,<3.5" boto3

    # systemd unit for MLflow (runs as 'ubuntu' user)
    cat >/etc/systemd/system/mlflow.service <<SERVICE
    [Unit]
    Description=MLflow Tracking Server
    After=network-online.target
    Wants=network-online.target

    [Service]
    Type=simple
    User=ubuntu
    WorkingDirectory=/var/mlflow
    Environment=AWS_DEFAULT_REGION=${var.region}
    ExecStart=/opt/mlflow/venv/bin/python -m mlflow server \
      --host 0.0.0.0 \
      --port 5000 \
      --backend-store-uri sqlite:////var/mlflow/mlflow.db \
      --default-artifact-root s3://${var.bucket_name}
    Restart=on-failure
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    SERVICE

    # Start the service
    systemctl daemon-reload
    systemctl enable --now mlflow
  EOF
}


resource "aws_instance" "mlflow" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.mlflow_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  user_data                   = local.user_data

  tags = { Name = "mlflow-ec2" }
}
