# EC2
module "ec2_instance" {
  source = "terraform-aws-modules/ec2-instance/aws"

  name = "emartapp-server"

  instance_type = var.instance_type
  # key_name                    = "emartapp-server-key"
  monitoring                  = true
  vpc_security_group_ids      = [module.sg.security_group_id]
  subnet_id                   = module.vpc.public_subnets[0]
  associate_public_ip_address = true
  user_data                   = file("user_data.sh")
  availability_zone           = data.aws_availability_zones.azs.names[0]

  tags = {
    Name        = "emartapp-server"
    Terraform   = "true"
    Environment = "dev"
  }
}
