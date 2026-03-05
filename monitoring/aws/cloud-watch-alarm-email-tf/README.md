# Demo: EC2 CPU Alarm → Email Notification

A Terraform demo that provisions an EC2 instance, simulates high CPU load, and sends an email alert via CloudWatch + SNS when CPU exceeds 80%.

## Architecture

```
EC2 (stress-ng → 100% CPU)
        ↓
CloudWatch Alarm (CPU > 80% for 2 minutes)
        ↓
SNS Topic
        ↓
Email notification
```

## What It Does

1. Creates a **t2.micro EC2** instance (Free Tier)
2. Installs `stress-ng` via `user_data` and runs it automatically after 2 minutes
3. Creates a **CloudWatch Alarm** that triggers when CPU > 80% for 2 consecutive periods
4. Sends an **email via SNS** when the alarm fires (and when it recovers)
5. Registers your local SSH public key in AWS automatically via Terraform

## Prerequisites

- AWS CLI configured (`aws configure`)
- Terraform >= 1.0
- An SSH key pair on your machine (e.g. `~/.ssh/my-key`)

## Project Structure

```
.
├── main.tf                  # EC2, VPC, SNS, CloudWatch Alarm
├── key_pair.tf              # AWS Key Pair from local public key
├── variables.tf             # Input variables
├── outputs.tf               # Useful outputs (IP, SSH command, alarm name)
├── terraform.tfvars.example # Example variable values
└── README.md
```

## Usage

### 1. Configure variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
aws_region      = "eu-west-1"
project_name    = "cpu-alarm-demo"
instance_type   = "t2.micro"
public_key_path = "~/.ssh/my-key.pub"   # path to your local public key
alert_email     = "your@email.com"      # email to receive alerts
cpu_threshold   = 80
evaluation_periods = 2
```

### 2. Deploy

```bash
terraform init
terraform plan
terraform apply
```

### 3. ⚠️ Confirm your email subscription!

After `terraform apply`, check your inbox for an email from `no-reply@sns.amazonaws.com` with subject:

> **AWS Notification - Subscription Confirmation**

Click **"Confirm subscription"** — without this step, alerts will NOT be delivered.

### 4. Wait for the alarm

| Time | What happens |
|------|-------------|
| 0 min | EC2 starts |
| +2 min | `stress-ng` launches (100% CPU for 10 min) |
| +4 min | CloudWatch detects 2 consecutive periods > 80% |
| +4 min | **ALARM email arrives** |
| +14 min | stress-ng stops, CPU drops |
| +16 min | **OK email arrives** (CPU recovered) |

### 5. Monitor alarm state

```bash
# Check current state
aws cloudwatch describe-alarms \
  --alarm-names "cpu-alarm-demo-high-cpu" \
  --query "MetricAlarms[0].StateValue" \
  --output text

# Watch continuously (every 30s)
watch -n 30 'aws cloudwatch describe-alarms \
  --alarm-names "cpu-alarm-demo-high-cpu" \
  --query "MetricAlarms[0].StateValue" \
  --output text'
```

### 6. SSH into the instance (optional)

```bash
# SSH command is printed as a Terraform output
ssh -i '~/.ssh/my-key' ec2-user@<PUBLIC_DNS>

# Check stress-ng is running
top
```

### 7. Trigger alarm manually (for testing)

```bash
aws cloudwatch set-alarm-state \
  --alarm-name "cpu-alarm-demo-high-cpu" \
  --state-value ALARM \
  --state-reason "Manual test"
```

## Cleanup

```bash
terraform destroy
```

Removes all resources: EC2, VPC, Subnet, Security Group, Internet Gateway, Route Table, Key Pair, SNS Topic, CloudWatch Alarm.

## Cost

| Resource | Cost |
|----------|------|
| EC2 t2.micro | **Free Tier** (750h/month) |
| CloudWatch Alarm | **Free** (first 10 alarms) |
| SNS Email | **Free** (first 1,000 emails/month) |

**Total demo cost: $0**

## Key Concepts Demonstrated

- **CloudWatch Metrics** — monitoring `CPUUtilization` from `AWS/EC2` namespace
- **CloudWatch Alarm** — threshold-based alerting with configurable evaluation periods
- **SNS Topic + Subscription** — pub/sub notification delivery to email
- **EC2 user_data** — bootstrapping scripts on instance launch
- **Terraform `aws_key_pair`** — importing local SSH public key into AWS programmatically
