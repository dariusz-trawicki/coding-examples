## WebSocket on ECS AWS

WebSocket server running in an ECS Fargate container behind an ALB, plus a lightweight client running locally.

Included in the project:
- `Terraform` (VPC, ALB, ECS, IAM roles, CloudWatch logs)
- `Dockerfile` and server code (Node + ws)
- simple `HTML/JS client`

#### File structure

```text
.
├─ server/
│  ├─ Dockerfile
│  └─ server.js
├─ client/
│  └─ index.html
└─ terraform/
   ├─ main.tf
   ├─ variables.tf
   └─ outputs.tf
```

### Quick start

1. Build and push the image (one-time setup):

```bash
cd server
# log Docker into your ECR registry
aws ecr get-login-password --region eu-central-1 \
  | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.eu-central-1.amazonaws.com

# Output:
# Login Succeeded

# run terraform apply first to create the ECR repo
cd ../terraform
terraform init
terraform apply
# Output example:
# alb_dns_name = "ws-demo-alb-455807830.eu-central-1.elb.amazonaws.com"
# ecr_repo_url = "253490761607.dkr.ecr.eu-central-1.amazonaws.com/ws-demo-repo"

# save the repo URL for Docker
export REPO_URL=$(terraform output -raw ecr_repo_url)

# build & push
cd ../server
# enable buildx
docker buildx create --use || true

# build and push a multi-arch image (amd64 + arm64)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ${REPO_URL}:latest \
  --push .
```

2. Update the ECS service after pushing the new image (first deployment or rollout):

```bash
# refresh ECS so it launches a new task with :latest
cd ../terraform
terraform apply -auto-approve
```

3. Get the ALB DNS and connect using the client:

```bash
terraform output alb_dns_name
# Output example:
# "ws-demo-alb-455807830.eu-central-1.elb.amazonaws.com"
```

4. Test

```bash
# Quick health check (after a short delay)
curl http://ws-demo-alb-455807830.eu-central-1.elb.amazonaws.com/health
# Output:
# {"ok":true}%

wscat -c ws://ws-demo-alb-455807830.eu-central-1.elb.amazonaws.com/ws
# # Output
# Connected (press CTRL+C to quit)
# < hello from ECS - WebSocket server!
# Disconnected (code: 1006, reason: "")
```

### Web client

In the browser:

For endpoint:
`ws://ws-demo-alb-455807830.eu-central-1.elb.amazonaws.com/ws`

- Connect button:
  - connected ✅
  - recv: hello from ECS - WebSocket server!

- Send "ping" button:
  - recv: echo: ping @ 2025-11-11T10:40:45.499Z