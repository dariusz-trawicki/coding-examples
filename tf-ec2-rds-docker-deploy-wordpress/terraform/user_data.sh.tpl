#!/bin/bash
set -e

# Update system and install basic dependencies
apt-get update -y
apt-get upgrade -y
apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# Add Docker's official GPG key and set up the repository
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and CLI
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Enable and start the Docker service
systemctl enable docker
systemctl start docker

# Add the default 'ubuntu' user to the 'docker' group
usermod -aG docker ubuntu

# Install Docker Compose (standalone binary)
DOCKER_COMPOSE_VERSION="v2.24.6"
curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Create the directory for docker-compose files
mkdir -p /home/ubuntu/wordpress
cd /home/ubuntu/wordpress

# Generate the docker-compose.yml file for WordPress
cat > docker-compose.yml <<EOF
version: '3.3'

services:
  wordpress:
    image: wordpress:latest
    ports:
      - "80:80"
    environment:
      WORDPRESS_DB_HOST: "${rds_host}:3306"
      WORDPRESS_DB_USER: "${rds_user}"
      WORDPRESS_DB_PASSWORD: "${rds_password}"
      WORDPRESS_DB_NAME: "${rds_dbname}"
    restart: always
EOF

# Adjust ownership and start the container as 'ubuntu' user
chown -R ubuntu:ubuntu /home/ubuntu/wordpress
su - ubuntu -c 'cd /home/ubuntu/wordpress && (docker compose up -d || docker-compose up -d)'
