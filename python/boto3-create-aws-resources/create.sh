#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install boto3

export AWS_REGION=eu-central-1
export BUCKET_NAME=python-created-bucket-12345
python create_and_upload.py
