#!/usr/bin/env bash
# create_network_sg_keypair_and_ec2.sh
# Creates a VPC, public subnet, IGW, RT, SG, Key Pair, and EC2 (with optional user-data).
# Requirements: AWS CLI v2, curl; profile/region in ~/.aws/config or via ENV.

# Script with optional user-data and, if you want, EIP attachment. 
# Everything is controlled via environment variables.

# How to use (example) in CLI: 
# here with user-data and EIP:

# chmod +x run.sh
# run in CLI (command below split into 3 lines for readability):
# USER_DATA_FILE=./web.sh USE_EIP=true MAP_PUBLIC_IP=false KEY_NAME=test-web-server-key /
# PUBLIC_KEY_PATH=~/.ssh/test-web-server-key.pub \
# bash run.sh

# - `MAP_PUBLIC_IP=true` → subnet assigns a public IP automatically (simpler).
# - `USE_EIP=true + MAP_PUBLIC_IP=false` → stable EIP address (recommended for production).
# - `USER_DATA_FILE` → path to a script to run at startup (optional).


set -euo pipefail

# ====== CONFIG (you can override with ENV) ======
REGION="${REGION:-eu-central-1}"
AZ="${AZ:-eu-central-1a}"
VPC_CIDR="${VPC_CIDR:-10.10.0.0/16}"
SUBNET_CIDR="${SUBNET_CIDR:-10.10.1.0/24}"

SG_NAME="${SG_NAME:-test-web-proj-sg}"

KEY_NAME="${KEY_NAME:-test-web-server-key}"
PUBLIC_KEY_PATH="${PUBLIC_KEY_PATH:-}"   # e.g. ~/.ssh/test-web-server-key.pub (if empty → create key pair in AWS)

# EC2
AMI_ID="${AMI_ID:-ami-0a116fa7c861dd5f9}"   # Ubuntu 22.04 LTS in eu-central-1 (change as needed)
# AMI_ID="${AMI_ID:-ami-015cbce10f839bd0c}"  # Amazon Linux 2023 in eu-central-1 (change as needed)
INSTANCE_TYPE="${INSTANCE_TYPE:-t3.micro}"
INSTANCE_NAME="${INSTANCE_NAME:-test-web-server}"
USER_DATA_FILE="${USER_DATA_FILE:-}"        # e.g. ./web.sh; if empty → no user-data

# Public network: auto-public IP on subnet (true) or EIP on instance (false + EIP)?
MAP_PUBLIC_IP="${MAP_PUBLIC_IP:-true}"      # true/false
USE_EIP="${USE_EIP:-false}"                 # if true → force AssociatePublicIpAddress=false and attach EIP

# SSH rule
ALLOW_SSH_CIDR="${ALLOW_SSH_CIDR:-}"       # e.g. "1.2.3.4/32"; if empty → will be detected

# ====== CHECKS ======
for cmd in aws curl; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Missing tool: $cmd"; exit 1; }
done

if [[ -z "$ALLOW_SSH_CIDR" ]]; then
  MY_IP="$(curl -s ifconfig.me || true)"
  [[ -n "$MY_IP" ]] || { echo "Public IP not detected. Set ALLOW_SSH_CIDR manually (e.g. 1.2.3.4/32)."; exit 1; }
  ALLOW_SSH_CIDR="${MY_IP}/32"
fi

echo "==> REGION=$REGION AZ=$AZ"
echo "==> VPC_CIDR=$VPC_CIDR SUBNET_CIDR=$SUBNET_CIDR"
echo "==> SG_NAME=$SG_NAME KEY_NAME=$KEY_NAME"
echo "==> AMI_ID=$AMI_ID INSTANCE_TYPE=$INSTANCE_TYPE NAME=$INSTANCE_NAME"
echo "==> MAP_PUBLIC_IP=$MAP_PUBLIC_IP USE_EIP=$USE_EIP"
echo "==> SSH from $ALLOW_SSH_CIDR"
echo

# ====== 1) VPC + IGW + SUBNET + RT ======
VPC_ID=$(aws ec2 create-vpc --region "$REGION" \
  --cidr-block "$VPC_CIDR" \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=test-web-vpc}]" \
  --query 'Vpc.VpcId' --output text)
aws ec2 modify-vpc-attribute --region "$REGION" --vpc-id "$VPC_ID" --enable-dns-support
aws ec2 modify-vpc-attribute --region "$REGION" --vpc-id "$VPC_ID" --enable-dns-hostnames

IGW_ID=$(aws ec2 create-internet-gateway --region "$REGION" \
  --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=test-web-igw}]" \
  --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --region "$REGION" --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"

SUBNET_ID=$(aws ec2 create-subnet --region "$REGION" \
  --vpc-id "$VPC_ID" --cidr-block "$SUBNET_CIDR" --availability-zone "$AZ" \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=test-web-public-$AZ}]" \
  --query 'Subnet.SubnetId' --output text)

if [[ "$MAP_PUBLIC_IP" == "true" ]]; then
  aws ec2 modify-subnet-attribute --region "$REGION" --subnet-id "$SUBNET_ID" --map-public-ip-on-launch
fi

RTB_ID=$(aws ec2 create-route-table --region "$REGION" --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=test-web-public-rt}]" \
  --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --region "$REGION" --route-table-id "$RTB_ID" \
  --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID"
aws ec2 associate-route-table --region "$REGION" --subnet-id "$SUBNET_ID" --route-table-id "$RTB_ID"

echo "VPC_ID=$VPC_ID SUBNET_ID=$SUBNET_ID RTB_ID=$RTB_ID IGW_ID=$IGW_ID"
echo

# ====== 2) SG (HTTP/HTTPS + SSH from /32 + EIC) ======
SG_ID=$(aws ec2 create-security-group --region "$REGION" \
  --group-name "$SG_NAME" --description "Web SG" --vpc-id "$VPC_ID" \
  --query 'GroupId' --output text)

aws ec2 authorize-security-group-ingress --region "$REGION" --group-id "$SG_ID" --protocol tcp --port 80  --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --region "$REGION" --group-id "$SG_ID" --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --region "$REGION" --group-id "$SG_ID" --protocol tcp --port 22  --cidr "$ALLOW_SSH_CIDR"

EIC_PL=$(aws ec2 describe-managed-prefix-lists --region "$REGION" \
  --filters "Name=prefix-list-name,Values=com.amazonaws.$REGION.ec2-instance-connect" \
  --query 'PrefixLists[0].PrefixListId' --output text || true)
if [[ -n "$EIC_PL" && "$EIC_PL" != "None" ]]; then
  aws ec2 authorize-security-group-ingress --region "$REGION" --group-id "$SG_ID" \
    --ip-permissions "IpProtocol=tcp,FromPort=22,ToPort=22,PrefixListIds=[{PrefixListId=$EIC_PL}]"
  echo "Added EC2 Instance Connect rule ($EIC_PL)."
fi
echo "SG_ID=$SG_ID"
echo

# ====== 3) KEY PAIR ======
if [[ -n "$PUBLIC_KEY_PATH" && -f "$PUBLIC_KEY_PATH" ]]; then
  echo "Importing public key → $KEY_NAME"
  aws ec2 import-key-pair --region "$REGION" --key-name "$KEY_NAME" \
    --public-key-material "fileb://${PUBLIC_KEY_PATH/#\~/$HOME}"
else
  echo "Creating Key Pair in AWS → $KEY_NAME (saving private key to ./${KEY_NAME}.pem)"
  aws ec2 create-key-pair --region "$REGION" --key-name "$KEY_NAME" \
    --query 'KeyMaterial' --output text > "${KEY_NAME}.pem"
  chmod 400 "${KEY_NAME}.pem"
fi
echo

# ====== 4) EC2 run-instances (+ optional user-data, + optional EIP) ======
# Decide whether to set AssociatePublicIpAddress on ENI
ASSOCIATE_PUBLIC="true"
if [[ "$USE_EIP" == "true" ]]; then
  ASSOCIATE_PUBLIC="false"
fi

RUN_ARGS=(
  --region "$REGION"
  --image-id "$AMI_ID"
  --instance-type "$INSTANCE_TYPE"
  --key-name "$KEY_NAME"
  --network-interfaces "[{\"DeviceIndex\":0,\"SubnetId\":\"$SUBNET_ID\",\"AssociatePublicIpAddress\":$ASSOCIATE_PUBLIC,\"Groups\":[\"$SG_ID\"]}]"
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]"
)
# user-data if provided
if [[ -n "$USER_DATA_FILE" ]]; then
  RUN_ARGS+=( --user-data "file://$USER_DATA_FILE" )
fi

INSTANCE_ID=$(aws ec2 run-instances "${RUN_ARGS[@]}" \
  --query 'Instances[0].InstanceId' --output text)
echo "EC2 created: INSTANCE_ID=$INSTANCE_ID"

aws ec2 wait instance-running --region "$REGION" --instance-ids "$INSTANCE_ID"

PUBLIC_IP=""
if [[ "$USE_EIP" == "true" ]]; then
  ALLOCATION_ID=$(aws ec2 allocate-address --region "$REGION" --domain vpc --query 'AllocationId' --output text)
  ASSOC_ID=$(aws ec2 associate-address --region "$REGION" --allocation-id "$ALLOCATION_ID" --instance-id "$INSTANCE_ID" --query 'AssociationId' --output text)
  PUBLIC_IP=$(aws ec2 describe-addresses --region "$REGION" --allocation-ids "$ALLOCATION_ID" --query 'Addresses[0].PublicIp' --output text)
  echo "EIP attached: $PUBLIC_IP (AllocationId=$ALLOCATION_ID, AssociationId=$ASSOC_ID)"
else
  # wait until PublicIpAddress appears
  for i in {1..20}; do
    PUBLIC_IP=$(aws ec2 describe-instances --region "$REGION" --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
    [[ "$PUBLIC_IP" != "None" && -n "$PUBLIC_IP" ]] && break || sleep 3
  done
fi

PRIVATE_IP=$(aws ec2 describe-instances --region "$REGION" --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].PrivateIpAddress' --output text)

echo
echo "==> DONE"
echo "INSTANCE_ID : $INSTANCE_ID"
echo "PUBLIC_IP   : ${PUBLIC_IP:-<none>}"
echo "PRIVATE_IP  : $PRIVATE_IP"
echo "SUBNET_ID   : $SUBNET_ID"
echo "SG_ID       : $SG_ID"
echo
[[ -n "$PUBLIC_IP" ]] && echo "HTTP:  http://$PUBLIC_IP"

# Determine proper private key file for SSH
if [[ -n "${PUBLIC_KEY_PATH:-}" ]]; then
  # you imported a public key → private key is the same base name without .pub (e.g. ~/.ssh/web-key)
  PRIVATE_SSH_KEY="${PUBLIC_KEY_PATH%.pub}"
else
  # key was created in AWS → private key saved locally as ./<KEY_NAME>.pem
  PRIVATE_SSH_KEY="./${KEY_NAME}.pem"
fi

# Expand ~ to home directory
PRIVATE_SSH_KEY="${PRIVATE_SSH_KEY/#\~/$HOME}"

# If the chosen file doesn't exist, but we have .pem in current dir – use .pem
if [[ ! -f "$PRIVATE_SSH_KEY" && -f "./${KEY_NAME}.pem" ]]; then
  PRIVATE_SSH_KEY="./${KEY_NAME}.pem"
fi

# Set secure permissions
chmod 400 "$PRIVATE_SSH_KEY"

echo "Using private key: $PRIVATE_SSH_KEY"

# print friendly SSH command
[[ -n "$PUBLIC_IP" ]] && echo "SSH :  ssh -i ${PRIVATE_SSH_KEY} ubuntu@$PUBLIC_IP"
