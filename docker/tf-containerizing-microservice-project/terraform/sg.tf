module "sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "emartapp-sg"
  description = "Security Group for emartapp Server"
  vpc_id      = module.vpc.vpc_id

  ingress_with_cidr_blocks = [
    # HTTP (nginx)
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      description = "HTTP"
      cidr_blocks = "0.0.0.0/0"
    },
    # (opcjonalne) Angular client
    {
      from_port   = 4200
      to_port     = 4200
      protocol    = "tcp"
      description = "Client"
      cidr_blocks = "0.0.0.0/0"
    },
    # (opcjonalne) Node API
    {
      from_port   = 5000
      to_port     = 5000
      protocol    = "tcp"
      description = "API"
      cidr_blocks = "0.0.0.0/0"
    },
    # (opcjonalne) Java webapi
    {
      from_port   = 9000
      to_port     = 9000
      protocol    = "tcp"
      description = "WebAPI"
      cidr_blocks = "0.0.0.0/0"
    },
    # SSH (rozważ zawęzić do swojego IP!)
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "SSH"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  egress_with_cidr_blocks = [{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = "0.0.0.0/0"
  }]

  tags = { Name = "emartapp-sg" }
}
