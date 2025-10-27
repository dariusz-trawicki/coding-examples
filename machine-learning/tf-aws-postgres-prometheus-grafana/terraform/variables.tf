# AWS region where resources will be created
variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "db_name" {
  type    = string
  default = "mltestdb"
}

variable "db_user_name" {
  type    = string
  default = "postgres"
}

variable "user_password" {
  type    = string
  default = "postgres"
}