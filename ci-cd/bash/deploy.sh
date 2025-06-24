#!/bin/bash
set -e

echo "Running terraform apply..."
terraform apply -auto-approve

echo "Syncing GitHub secrets..."
./dev-sync-gh-secrets.sh


echo "Triggering GitHub Actions workflow..."

# parameters
REPO=$(terraform output -raw github_repository)
REF="main"
WORKFLOW_FILE="dev-deploy.yaml"

# Run GitHub action
gh workflow run "$WORKFLOW_FILE" \
  --repo "$REPO" \
  --ref "$REF"

echo "GitHub Actions triggered."
