#!/bin/bash

set -e

CA_FILE="./global-bundle.pem"
TEMP_DIR="/tmp/db-data"
MONGO_URI="mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@${MONGO_URL}:27017/${DB_NAME}?tls=true&retryWrites=false&tlsCAFile=${CA_FILE}"

echo "⬇️ Syncing data from S3..."
mkdir -p "$TEMP_DIR"
aws s3 sync "s3://${S3_BUCKET_NAME}/${S3_PREFIX}" "$TEMP_DIR"

collections=(xxx yyy zzz aaa bbb ccc)

echo "Dropping old collections..."
for col in "${collections[@]}"; do
  echo "Dropping $col"
  mongosh "$MONGO_URI" --eval "db.getCollection('$col').drop()" || true
done

echo "Importing data..."
for col in "${collections[@]}"; do
  FILE="$TEMP_DIR/xxxxxxxx.${col}.json"
  echo "Importing $col from $FILE"
  mongoimport --uri="$MONGO_URI" --collection="$col" --file="$FILE" --jsonArray || echo "Failed $col"
done

echo "All done."
