# Using the boto3 library to work with Amazon S3

**boto3** is `Amazon’s` official `Python SDK` for talking to `AWS` (`Amazon Web Services`).

#### What the example does

`create_and_upload.py` - creates an `S3` bucket and uploads a sample `file.txt`.

`delete_bucket_and_contents.py` - deletes all objects/versions and removes the bucket.

#### RUN

Set the `BUCKET_NAME` value in `create.sh` and `delete.sh` scripts.

NOTE: Bucket names must be globally `unique` (lowercase letters, numbers, hyphens).

```bash
chmod +x create.sh
chmod +x delete.sh
./create.sh   # create s3
./delete.sh   # delete s3
```

