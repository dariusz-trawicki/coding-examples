# VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "emartapp-vpc"
  cidr = var.vpc_cidr

  azs                     = data.aws_availability_zones.azs.names
  public_subnets          = var.public_subnets
  map_public_ip_on_launch = true

  enable_dns_hostnames = true

  tags = {
    Name        = "emartapp-vpc"
    Terraform   = "true"
    Environment = "dev"
  }

  public_subnet_tags = {
    Name = "emartapp-subnet"
  }
}
