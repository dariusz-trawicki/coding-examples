#!/usr/bin/env bash
# clean.sh
# Removes: EC2 (+EIP), Key Pair, SG, RT associations, RT, Subnet, IGW, VPC.
# Assumes names/tags as in our creation scripts:
#   VPC Name=test-web-vpc
#   IGW Name=web-igw
#   Subnet Name=test-web-public-$AZ
#   Route Table Name=test-web-public-rt
#   Security Group name = $SG_NAME
#   EC2 tag Name = $INSTANCE_NAME
#
# Usage:
#   bash clean.sh
# Or with overrides:
#   REGION=eu-central-1 AZ=eu-central-1a SG_NAME=test-web-proj-sg KEY_NAME=test-web-server-key INSTANCE_NAME=test-web-server \
#   VPC_NAME=test-web-vpc SUBNET_NAME=test-web-public-eu-central-1a RTB_NAME=test-web-public-rt IGW_NAME=web-igw \
#   bash clean.sh

set -euo pipefail

REGION="${REGION:-eu-central-1}"
AZ="${AZ:-eu-central-1a}"

# Names/Tags (you can override via env vars above)
VPC_NAME="${VPC_NAME:-test-web-vpc}"
IGW_NAME="${IGW_NAME:-test-web-igw}"
SUBNET_NAME="${SUBNET_NAME:-test-web-public-$AZ}"
RTB_NAME="${RTB_NAME:-test-web-public-rt}"
SG_NAME="${SG_NAME:-test-web-proj-sg}"
KEY_NAME="${KEY_NAME:-test-web-server-key}"
INSTANCE_NAME="${INSTANCE_NAME:-test-web-server}"

echo "==> Region: $REGION | AZ: $AZ"
echo "==> Looking for resources by names/tags…"

# ---- Detecting resource IDs ----
VPC_ID="${VPC_ID:-$(aws ec2 describe-vpcs --region "$REGION" \
  --filters "Name=tag:Name,Values=$VPC_NAME" \
  --query 'Vpcs[0].VpcId' --output text 2>/dev/null || true)}"

SUBNET_ID="${SUBNET_ID:-$(aws ec2 describe-subnets --region "$REGION" \
  --filters "Name=tag:Name,Values=$SUBNET_NAME" "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[0].SubnetId' --output text 2>/dev/null || true)}"

RTB_ID="${RTB_ID:-$(aws ec2 describe-route-tables --region "$REGION" \
  --filters "Name=tag:Name,Values=$RTB_NAME" "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[0].RouteTableId' --output text 2>/dev/null || true)}"

IGW_ID="${IGW_ID:-$(aws ec2 describe-internet-gateways --region "$REGION" \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=$IGW_NAME" \
  --query 'InternetGateways[0].InternetGatewayId' --output text 2>/dev/null || true)}"

SG_ID="${SG_ID:-$(aws ec2 describe-security-groups --region "$REGION" \
  --filters "Name=group-name,Values=$SG_NAME" "Name=vpc-id,Values=$VPC_ID" \
  --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null || true)}"

# EC2 by tag Name=INSTANCE_NAME in the given VPC (all states except terminated)
INSTANCE_IDS_RAW="$(aws ec2 describe-instances --region "$REGION" \
  --filters "Name=tag:Name,Values=$INSTANCE_NAME" "Name=network-interface.vpc-id,Values=$VPC_ID" \
             "Name=instance-state-name,Values=pending,running,stopping,stopped" \
  --query 'Reservations[].Instances[].InstanceId' --output text 2>/dev/null || true)"
# Normalization
INSTANCE_IDS=()
for id in $INSTANCE_IDS_RAW; do [[ "$id" != "None" && -n "$id" ]] && INSTANCE_IDS+=("$id"); done

for var in VPC_ID SUBNET_ID RTB_ID IGW_ID SG_ID; do
  [[ "${!var:-}" == "None" ]] && declare "$var"=""
done

echo "VPC_ID      = ${VPC_ID:-<not found>}"
echo "SUBNET_ID   = ${SUBNET_ID:-<not found>}"
echo "RTB_ID      = ${RTB_ID:-<not found>}"
echo "IGW_ID      = ${IGW_ID:-<not found>}"
echo "SG_ID       = ${SG_ID:-<not found>}"
echo "KEY_NAME    = ${KEY_NAME:-<not set>}"
echo "INSTANCE(S) = ${INSTANCE_IDS[*]:-<none>}"
echo

# ---- 1) EIP → disassociate + release (for EIPs attached to detected instances) ----
if ((${#INSTANCE_IDS[@]})); then
  echo "-> Finding and releasing EIPs attached to instances…"
  for IID in "${INSTANCE_IDS[@]}"; do
    ASSOC_JSON="$(aws ec2 describe-addresses --region "$REGION" \
      --filters "Name=instance-id,Values=$IID" --query 'Addresses[0]' --output json 2>/dev/null || true)"
    if [[ "$ASSOC_JSON" != "null" && -n "$ASSOC_JSON" ]]; then
      ALLOC_ID="$(echo "$ASSOC_JSON" | jq -r '.AllocationId // empty')"
      ASSOC_ID="$(echo "$ASSOC_JSON" | jq -r '.AssociationId // empty')"
      PUB_IP="$(echo "$ASSOC_JSON"   | jq -r '.PublicIp // empty')"
      if [[ -n "$ASSOC_ID" ]]; then
        echo "   - Disassociate $PUB_IP ($ASSOC_ID)"
        aws ec2 disassociate-address --region "$REGION" --association-id "$ASSOC_ID" || true
      fi
      if [[ -n "$ALLOC_ID" ]]; then
        echo "   - Release $PUB_IP ($ALLOC_ID)"
        aws ec2 release-address --region "$REGION" --allocation-id "$ALLOC_ID" || true
      fi
    fi
  done
fi

# ---- 2) EC2 terminate (if any) ----
if ((${#INSTANCE_IDS[@]})); then
  echo "-> Terminating instances: ${INSTANCE_IDS[*]}"
  aws ec2 terminate-instances --region "$REGION" --instance-ids "${INSTANCE_IDS[@]}" >/dev/null
  aws ec2 wait instance-terminated --region "$REGION" --instance-ids "${INSTANCE_IDS[@]}"
  echo "   Instances terminated."
fi

# ---- 3) Key Pair (AWS) ----
# Use KEY_NAME from ENV; if missing, try to guess from .pem in current directory
if [[ -z "${KEY_NAME:-}" ]]; then
  CAND=$(ls -1 *.pem 2>/dev/null | head -n1 | sed 's/\.pem$//')
  [[ -n "$CAND" ]] && KEY_NAME="$CAND"
fi

if [[ -n "${KEY_NAME:-}" ]]; then
  echo "-> Deleting Key Pair: $KEY_NAME"
  # try by ID (more precise); if not found – try by name
  KP_ID=$(aws ec2 describe-key-pairs --region "$REGION" \
    --key-names "$KEY_NAME" --query 'KeyPairs[0].KeyPairId' --output text 2>/dev/null || true)

  if [[ -n "$KP_ID" && "$KP_ID" != "None" ]]; then
    aws ec2 delete-key-pair --region "$REGION" --key-pair-id "$KP_ID" || true
  else
    aws ec2 delete-key-pair --region "$REGION" --key-name "$KEY_NAME" || true
  fi
else
  echo "(!) KEY_NAME not set and no *.pem found — skipping Key Pair deletion."
fi

# Remove local private key file (if it was created by the script)
if [[ -n "${KEY_NAME:-}" && -f "./${KEY_NAME}.pem" ]]; then
  chmod u+w "./${KEY_NAME}.pem" 2>/dev/null || true
  rm -f "./${KEY_NAME}.pem"
  echo "Removed local key: ./${KEY_NAME}.pem"
fi

# ---- 4) Security Group ----
if [[ -n "${SG_ID:-}" ]]; then
  echo "-> Deleting Security Group: $SG_ID"
  aws ec2 delete-security-group --region "$REGION" --group-id "$SG_ID" || true
fi

# ---- 5) Route Table: disassociate (non-main) + delete ----
if [[ -n "${RTB_ID:-}" ]]; then
  echo "-> Removing RT associations: $RTB_ID"
  ASSOC_IDS=$(aws ec2 describe-route-tables --region "$REGION" \
    --route-table-ids "$RTB_ID" \
    --query 'RouteTables[0].Associations[?Main==`false`].RouteTableAssociationId' \
    --output text 2>/dev/null || true)
  for AID in $ASSOC_IDS; do
    [[ -n "$AID" ]] && aws ec2 disassociate-route-table --region "$REGION" --association-id "$AID" || true
  done
  echo "-> Deleting RT: $RTB_ID"
  aws ec2 delete-route-table --region "$REGION" --route-table-id "$RTB_ID" || true
fi

# ---- 6) Subnet ----
if [[ -n "${SUBNET_ID:-}" ]]; then
  echo "-> Deleting Subnet: $SUBNET_ID"
  aws ec2 delete-subnet --region "$REGION" --subnet-id "$SUBNET_ID" || true
fi

# ---- 7) IGW: detach + delete ----
if [[ -n "${IGW_ID:-}" && -n "${VPC_ID:-}" ]]; then
  echo "-> Detaching and deleting IGW: $IGW_ID"
  aws ec2 detach-internet-gateway --region "$REGION" --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID" || true
  aws ec2 delete-internet-gateway --region "$REGION" --internet-gateway-id "$IGW_ID" || true
fi

# ---- 8) VPC ----
if [[ -n "${VPC_ID:-}" ]]; then
  echo "-> Deleting VPC: $VPC_ID"
  aws ec2 delete-vpc --region "$REGION" --vpc-id "$VPC_ID" || true
fi

echo
echo "==> Cleanup finished."
