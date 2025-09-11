import os
import boto3
from botocore.exceptions import ClientError

region = os.environ.get("AWS_REGION", "eu-central-1")
bucket_name = os.environ["BUCKET_NAME"]  # set this env var
key = os.environ.get("KEY", "file.txt")  # optional: object to mention in logs

s3 = boto3.resource("s3", region_name=region)
s3c = boto3.client("s3", region_name=region)
bucket = s3.Bucket(bucket_name)

def bucket_exists(name: str) -> bool:
    try:
        s3c.head_bucket(Bucket=name)
        return True
    except ClientError as e:
        code = e.response["Error"]["Code"]
        return code in ("404", "NoSuchBucket", "NotFound")

if not bucket_exists(bucket_name):
    print(f"Bucket not found: s3://{bucket_name}")
    raise SystemExit(0)

print(f"Emptying bucket: s3://{bucket_name} (including versions & delete markers)…")
# Works for both versioned and unversioned buckets:
bucket.object_versions.delete()

print(f"Deleting bucket: s3://{bucket_name} …")
bucket.delete()
print("Deleted.")
