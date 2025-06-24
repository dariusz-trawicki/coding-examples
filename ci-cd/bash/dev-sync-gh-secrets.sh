#!/bin/bash
set -e

# Get values from Terraform outputs
aws_account_id=$(terraform output -raw aws_account_id)
aws_region=$(terraform output -raw aws_region)
mongo_url=$(terraform output -raw docdb_endpoint_mongodb_url)
bucket_name=$(terraform output -raw bucket_name)


echo "Setting GitHub secrets for repo: $github_repository"

gh secret set DEV_AWS_REGION                          --repo "$github_repository" --body "$aws_region"
gh secret set DEV_AWS_ACCOUNT_ID                      --repo "$github_repository" --body "$aws_account_id"
gh secret set DEV_MONGO_URL                           --repo "$github_repository" --body "$mongo_url"
gh secret set DEV_S3_BUCKET_NAME                      --repo "$github_repository" --body "$bucket_name"

echo "All secrets synced successfully."
