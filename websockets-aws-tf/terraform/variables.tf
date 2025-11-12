variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "AWS region"
}

variable "project_name" {
  type    = string
  default = "ws-demo"
}

variable "desired_count" {
  type    = number
  default = 1
}
