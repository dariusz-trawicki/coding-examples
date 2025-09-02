# 1) Generate a key pair
resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# 2) Save the private key locally (do not commit!)
resource "local_file" "private_key" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.module}/${var.key_pair_filename}" # e.g. "server-key.pem"
  file_permission = "0400"
}

# 3) Register the public key in AWS as a Key Pair
resource "aws_key_pair" "ssh_key" {
  key_name   = var.aws_key_pair_name # e.g. "server-key"
  public_key = tls_private_key.ssh.public_key_openssh
}