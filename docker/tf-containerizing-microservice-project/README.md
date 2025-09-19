## Containerizing microservice project (build and run)

This project demonstrates how to provision cloud infrastructure with `Terraform` and deploy a `microservices-based application` on an `EC2` instance in AWS.

The workflow is as follows:

- **Infrastructure provisioning** – `Terraform` creates the required networking resources (VPC, subnets, security groups) and an EC2 instance.

- **Instance initialization** – A user data script installs `Docker` and `Docker Compose` on the `EC2` instance.

- **Application deployment** – The `EC2` instance automatically clones the `emartapp repository` and starts the microservices stack (API, client, databases, and Nginx reverse proxy) with `Docker Compose`.

This setup provides a simple but complete example of deploying a microservices architecture in the cloud.

#### Run

```bash
cd terraform

terraform init
terraform apply
# *** output (example) ***
# ec2_public_ip = "18.158.61.1"
```

Wait, this process may take a while... Open in the browser: http://18.158.61.1.


#### Cleanup

```bash
terraform destroy
```
