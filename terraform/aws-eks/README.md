# AWS: EKS Cluster example

## RUN

- Terraform:

```bash
cd terraform
terraform init
terraform apply
```

- Config `kubectl`:
aws eks --region eu-central-1 update-kubeconfig --name demo
