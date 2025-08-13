#!/usr/bin/env bash
# Purpose: build and run the Aqua Nova example site in Docker
# Modes:
#   - tar   : package app sources into aqua.tar.gz before building
#   - plain : use uncompressed sources directly
# Usage:
#   chmod +x run.sh
#   ./run.sh tar
#   ./run.sh plain

set -euo pipefail

# ===== Configuration =====
APP_URL="https://www.tooplate.com/zip-templates/2138_aqua_nova.zip"
ZIP_NAME="2138_aqua_nova.zip"
EXTRACT_DIR="2138_aqua_nova"

IMAGE="aqua_img"
CONTAINER="aquawebsite"
PORT=9080

# First script argument selects the mode; default to "tar"
MODE="${1:-tar}"
# =========================

# Ensure required CLI tools are present
need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
need curl; need unzip; need docker; need tar

# Stop & remove an existing container with the same name (if any)
stop_rm_container() {
  if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER}\$"; then
    echo "Removing existing container: ${CONTAINER}"
    docker rm -f "${CONTAINER}" >/dev/null || true
  fi
}

# Build the image (optionally with a tag) and run the container mapped to PORT->80
build_and_run() {
  local tag="${1:-latest}"

  echo "==> Building image: ${IMAGE}:${tag}"
  if [[ "${tag}" == "latest" ]]; then
    docker build -t "${IMAGE}" .
  else
    docker build -t "${IMAGE}:${tag}" .
  fi

  stop_rm_container

  echo "==> Starting container: ${CONTAINER} (host ${PORT} -> container 80)"
  if [[ "${tag}" == "latest" ]]; then
    docker run -d --name "${CONTAINER}" -p ${PORT}:80 "${IMAGE}"
  else
    docker run -d --name "${CONTAINER}" -p ${PORT}:80 "${IMAGE}:${tag}"
  fi

  # Show the container we just launched
  docker ps -a --filter "name=${CONTAINER}"
}

case "${MODE}" in
  tar)
    WORKDIR="aqua-tar"
    mkdir -p "${WORKDIR}"
    # Use the Dockerfile tailored for tar-based build context
    cp -f Dockerfile-tar "${WORKDIR}/Dockerfile"
    cd "${WORKDIR}"

    echo "==> Downloading and extracting the example app"
    curl -L -o "${ZIP_NAME}" "${APP_URL}"
    unzip -q "${ZIP_NAME}"
    rm -f "${ZIP_NAME}"

    echo "==> Creating compressed build context: aqua.tar.gz"
    ( cd "${EXTRACT_DIR}" && tar czvf aqua.tar.gz * )
    mv -f "${EXTRACT_DIR}/aqua.tar.gz" .
    rm -rf "${EXTRACT_DIR}"

    # Build & run "latest", then build & run a second tag to demonstrate tagging
    build_and_run "latest"
    echo "==> Rebuilding with tag V2"
    docker rm -f "${CONTAINER}" >/dev/null || true
    build_and_run "V2"
    ;;

  plain|not-tar|not)
    WORKDIR="aqua-not-tar"
    mkdir -p "${WORKDIR}"
    # Use the Dockerfile for plain (uncompressed) sources
    cp -f Dockerfile-not-tar "${WORKDIR}/Dockerfile"
    cd "${WORKDIR}"

    echo "==> Downloading and extracting the example app"
    curl -L -o "${ZIP_NAME}" "${APP_URL}"
    unzip -q "${ZIP_NAME}"
    rm -f "${ZIP_NAME}"

    echo "==> Copying sources into the build context"
    cp -a "${EXTRACT_DIR}/." .
    rm -rf "${EXTRACT_DIR}"

    build_and_run "latest"
    echo "==> Rebuilding with tag V3"
    docker rm -f "${CONTAINER}" >/dev/null || true
    build_and_run "V3"
    ;;

  *)
    echo "Usage: $0 [tar|plain]" >&2
    exit 1
    ;;
esac

echo "==> Done. Open in your browser: http://localhost:${PORT}"
