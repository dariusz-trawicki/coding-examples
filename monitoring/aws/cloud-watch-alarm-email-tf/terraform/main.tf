# ============================================================
# DEMO: EC2 + CloudWatch Alarm + SNS Email Alert
# ============================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ------------------------------------------------------------
# DATA: Fetch the latest Amazon Linux 2023 AMI
# ------------------------------------------------------------
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ------------------------------------------------------------
# NETWORK: VPC + Subnet + Security Group
# ------------------------------------------------------------
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags                 = { Name = "${var.project_name}-vpc" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-igw" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.project_name}-subnet" }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = { Name = "${var.project_name}-rt" }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.main.id
}

resource "aws_security_group" "ec2" {
  name        = "${var.project_name}-sg"
  description = "Allow SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # In production: restrict to your IP
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-sg" }
}


# ------------------------------------------------------------
# Key pair for EC2 access
# ------------------------------------------------------------
resource "aws_key_pair" "demo" {
  key_name   = var.aws_key_name
  public_key = file(var.public_key_path)
}


# ------------------------------------------------------------
# EC2: Instance with user_data for CPU load simulation
# ------------------------------------------------------------
resource "aws_instance" "demo" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.ec2.id]
  key_name               = aws_key_pair.demo.key_name

  # Stress test – will run automatically on startup
  # WARNING: generates 100% CPU for 10 minutes → alarm will trigger!
  user_data = <<-EOF
    #!/bin/bash
    yum install -y stress-ng
    echo "Wait 2 minutes, then the stress test will start..."
    sleep 120
    stress-ng --cpu 1 --timeout 600s &
  EOF

  monitoring = true # Detailed monitoring (every 1 min)

  tags = { Name = "${var.project_name}-ec2" }
}

# ------------------------------------------------------------
# SNS: Topic + Email subscription
# ------------------------------------------------------------
resource "aws_sns_topic" "cpu_alert" {
  name = "${var.project_name}-cpu-alert"
  tags = { Name = "${var.project_name}-sns" }
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.cpu_alert.arn
  protocol  = "email"
  endpoint  = var.alert_email

  # IMPORTANT: After terraform apply, check your email and click "Confirm subscription"
}

# ------------------------------------------------------------
# CLOUDWATCH ALARM: CPU > 80%
# ------------------------------------------------------------
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name        = "${var.project_name}-high-cpu"
  alarm_description = "CPU exceeded ${var.cpu_threshold}% for ${var.evaluation_periods} periods"

  # Metric
  metric_name = "CPUUtilization"
  namespace   = "AWS/EC2"
  statistic   = "Average"
  period      = 60 # every 1 minute (requires detailed monitoring)

  # Condition
  comparison_operator = "GreaterThanThreshold"
  threshold           = var.cpu_threshold
  evaluation_periods  = var.evaluation_periods

  # Link to EC2
  dimensions = {
    InstanceId = aws_instance.demo.id
  }

  # Actions
  alarm_actions = [aws_sns_topic.cpu_alert.arn] # email when ALARM
  ok_actions    = [aws_sns_topic.cpu_alert.arn] # email when back to OK

  # Treat missing data as OK (instance may be stopped)
  treat_missing_data = "notBreaching"

  tags = { Name = "${var.project_name}-alarm" }
}
