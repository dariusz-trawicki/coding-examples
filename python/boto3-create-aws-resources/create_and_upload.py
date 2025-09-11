# create_and_upload.py
import os, uuid, boto3

region = os.environ.get("AWS_REGION", "eu-central-1")
bucket = os.environ.get("BUCKET_NAME", f"demo-bucket-{uuid.uuid4().hex[:8]}-{region}")
key = "file.txt"
local_file = "file.txt"

s3_client = boto3.client("s3", region_name=region)

# 1) Create the bucket (special case for us-east-1)
params = {"Bucket": bucket}
if region != "us-east-1":
    params["CreateBucketConfiguration"] = {"LocationConstraint": region}
s3_client.create_bucket(**params)

# Wait until the bucket actually exists
s3_client.get_waiter("bucket_exists").wait(Bucket=bucket)

# 2) Create a local sample file
with open(local_file, "w", encoding="utf-8") as f:
    f.write("This is a sample file uploaded with boto3.\n")

# 3) Upload the file
s3 = boto3.resource("s3", region_name=region)
s3.Bucket(bucket).upload_file(local_file, key)

# (Optional) Generate a presigned URL to download the file (valid for 15 minutes)
url = s3_client.generate_presigned_url(
    "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=900
)

print(f"Bucket: s3://{bucket}")
print(f"Object: s3://{bucket}/{key}")
print(f"Presigned download URL (15 min): {url}")
