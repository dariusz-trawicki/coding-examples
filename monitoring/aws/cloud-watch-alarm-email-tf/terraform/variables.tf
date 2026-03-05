variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Prefix for all resources"
  type        = string
  default     = "cpu-alarm-demo"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro" # Free tier!
}

variable "alert_email" {
  description = "Email address to receive alerts"
  type        = string
  # "xxx@example.com"
}

variable "cpu_threshold" {
  description = "CPU threshold in % that triggers the alarm"
  type        = number
  default     = 80
}

variable "evaluation_periods" {
  description = "Number of consecutive periods that must exceed the threshold"
  type        = number
  default     = 2
}

variable "public_key_path" {
  description = "Path to the local public key"
  type        = string
  default     = "~/.ssh/test-key.pub"
}

variable "aws_key_name" {
  description = "SSH key name in AWS"
  type        = string
  default     = "test-key"
}
