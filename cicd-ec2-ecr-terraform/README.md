# CI/CD Pipeline with GitHub Actions and Terraform for AWS (OIDC + Terraform + Docker)

#### Source Code

The complete project is hosted on GitHub:  
[dariusz-trawicki/cicd-ec2-ecr-terraform](https://github.com/dariusz-trawicki/cicd-ec2-ecr-terraform)


---

This project demonstrates how to deploy a **Dockerized application** to an **EC2 instance** using **GitHub Actions** and **Terraform** with **OIDC authentication**.

#### Key components
- **Terraform** code to provision AWS resources (`EC2`, `ECR`, `IAM roles`).  
- **GitHub Actions** workflow to build and push Docker images to `ECR`, and deploy them on an `EC2` instance configured to run Docker and pull images from `ECR`.