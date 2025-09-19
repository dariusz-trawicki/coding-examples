# Deploying WordPress on AWS with Terraform, EC2, and RDS

In this project, we use `Terraform` to provision a simple `WordPress` environment on `AWS`. The deployment consists of an `EC2` instance running WordPress inside a `Docker` container and an `RDS` instance running `MySQL` as the database backend.

#### Key points

**Official WordPress Docker image**
Example uses the `official WordPress image` from `Docker Hub`. This image already includes a fully configured `Apache web server` and `PHP`, so the container can run `WordPress` immediately.

**Database requirement**
`WordPress` needs a `database` connection during startup. In our setup, this is provided by an `Amazon RDS` instance (`MySQL`). The `WordPress` container must know:
- Database `host` (`RDS endpoint` + port),
- Database `user`,
- Database `password`,
- Database `name`.

**Dynamic user-data generation**
Since the `RDS instance endpoint` is only available after `Terraform` creates the `DB`, we cannot hardcode these values in advance. To solve this:
- We prepare a `template` file `user_data.sh.tpl` that defines environment variables for the `WordPress` container.
- Terraform’s `templatefile()` function fills in the values dynamically after the `RDS` instance is created.

Example snippet from `user_data.sh.tpl` (inside `docker-compose.yml`):

```yaml
environment:
  WORDPRESS_DB_HOST: "${rds_host}:3306"
  WORDPRESS_DB_USER: "${rds_user}"
  WORDPRESS_DB_PASSWORD: "${rds_password}"
  WORDPRESS_DB_NAME: "${rds_dbname}"
```

**Passing variables in Terraform**
In `ec2.tf`, we attach the dynamically rendered script as `EC2 user data`:

```hcl
user_data = templatefile("${path.module}/user_data.sh.tpl", {
  rds_host     = aws_db_instance.wordpress.address   # RDS endpoint
  rds_user     = var.db_user_name
  rds_password = var.db_password
  rds_dbname   = var.db_name
  # DOCKER_COMPOSE_VERSION = "v2.24.6"
})
```

#### RUN

```bash
cd terraform
terraform init
terraform apply
# Example outputs:
# RDSEndpoint = "wp-instance.c34keo06inrq.eu-central-1.rds.amazonaws.com:3306"
# WebPublicIP = "3.65.176.30"
```

#### Tests
Wait, this process may take a while... Open in browser: http://3.65.176.30. You should see the WordPress installation page.

To log in to the EC2 instance via SSH:

```bash
ssh -i ./server-key.pem ubuntu@3.65.176.30
docker ps
```

#### Cleanup

```bash
terraform destroy
```
