#!/bin/bash
set -euxo pipefail

TEMPLATE_URL="https://www.tooplate.com/zip-templates/2119_gymso_fitness.zip"

# --- Install & enable web server + tools ---
if command -v apt-get >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y apache2 wget unzip curl
  systemctl enable --now apache2
  WEB_SVC="apache2"
elif command -v dnf >/dev/null 2>&1 || command -v yum >/dev/null 2>&1; then
  PKG_MGR="$(command -v dnf || command -v yum)"
  $PKG_MGR -y install httpd wget unzip curl
  systemctl enable --now httpd
  WEB_SVC="httpd"
else
  echo "Unsupported OS (need apt-get or dnf/yum)"; exit 1
fi

# --- Download & deploy template ---
WORKDIR="/tmp/site"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Download ZIP (curl with wget fallback)
curl -fL -o theme.zip "$TEMPLATE_URL" || wget -O theme.zip "$TEMPLATE_URL"

unzip -oq theme.zip

# Find the extracted directory (e.g., 2119_gymso_fitness) and copy it to /var/www/html
SRC_DIR="$(find . -maxdepth 1 -type d -name '2119_*' | head -n 1)"
: "${SRC_DIR:=.}"

rm -rf /var/www/html/*
cp -r "${SRC_DIR}/"* /var/www/html/

# File ownership (www-data for Debian/Ubuntu, apache for RHEL/Amazon Linux)
if id -u www-data >/dev/null 2>&1; then
  chown -R www-data:www-data /var/www/html || true
elif id -u apache >/dev/null 2>&1; then
  chown -R apache:apache /var/www/html || true
fi

# --- Restart web server ---
systemctl restart "$WEB_SVC"
