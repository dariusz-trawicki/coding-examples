#!/bin/bash
set -euxo pipefail

# Update system
sudo yum update -y

sudo dnf update -y
sudo dnf install -y docker git
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user
newgrp docker

# Install Docker Compose v2
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose


until docker info >/dev/null 2>&1; do
  sleep 1
done

# Clone the application repository and start the application
cd /home/ec2-user
if [ ! -d emartapp ]; then
  git clone https://github.com/dariusz-trawicki/emartapp.git
fi
cd emartapp
docker compose up -d
