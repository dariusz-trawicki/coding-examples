variable "region" {
  type        = string
  description = "AWS region to deploy resources in."
  default     = "eu-central-1"
}

variable "zone1" {
  type        = string
  description = "Preferred Availability Zone within aws_region (e.g., eu-central-1a)."
  default     = "eu-central-1a"
}

variable "zone2" {
  type        = string
  description = "Preferred Availability Zone within aws_region (e.g., eu-central-1a)."
  default     = "eu-central-1b"
}


variable "project_name" {
  type        = string
  description = "Project name for tagging resources."
  default     = "project"
}


variable "instance_name" {
  type        = string
  description = "Name tag for the EC2 instance."
  default     = "instance"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type (e.g., t3.micro)."
  default     = "t3.micro"
}

variable "ami_id" {
  type        = string
  description = "Pinned AMI ID for the chosen region (e.g., Ubuntu 22.04 LTS in eu-central-1)."
  default     = ""
}

variable "sg_name" {
  type        = string
  description = "Pinned AMI ID for the chosen region (e.g., Ubuntu 22.04 LTS in eu-central-1)."
  default     = "proj-sg"
}

variable "aws_key_pair_name" {
  type        = string
  description = "Name of the EC2 key pair to create (in the target AWS region)."
  default     = "keypair"
}

variable "key_pair_filename" {
  type        = string
  description = "Filename for the private key of the EC2 key pair (e.g., keypair.pem)."
  default     = "keypair.pem"
}

variable "rds_identifier" {
  type        = string
  description = "RDS instance identifier."
  default     = "rds-instance"
}

variable "db_name" {
  type        = string
  description = "Name of the initial database to create."
  default     = "mydatabase"
}

variable "db_engine" {
  type        = string
  description = "Database engine for RDS instance."
  default     = "mysql"
}

variable "db_user_name" {
  type        = string
  description = "Master username for the RDS instance."
  default     = "admin"
}

variable "db_password" {
  type        = string
  description = "Master password for the RDS instance."
  sensitive   = true
  default     = "Admin123$"
}

