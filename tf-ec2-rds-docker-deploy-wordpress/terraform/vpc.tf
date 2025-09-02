#vpc
resource "aws_vpc" "this" {
  cidr_block = "10.100.0.0/16"
  tags = {
    Name = "wp-vpc"
  }
}

#public subnets
resource "aws_subnet" "public1" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.100.1.0/24"
  availability_zone = var.zone1

  tags = {
    Name = "wp-public-1"
  }
}
resource "aws_subnet" "public2" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.100.2.0/24"
  availability_zone = var.zone2

  tags = {
    Name = "wp-public-2"
  }
}

#private subnets
resource "aws_subnet" "private1" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.100.3.0/24"
  availability_zone = var.zone1

  tags = {
    Name = "wp-private-1"
  }
}
resource "aws_subnet" "private2" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.100.4.0/24"
  availability_zone = var.zone2

  tags = {
    Name = "wp-private-2"
  }
}