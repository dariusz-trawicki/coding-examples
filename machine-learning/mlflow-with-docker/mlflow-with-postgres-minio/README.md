### Runs an `MLflow tracking server` with PostgreSQL and MinIO

Runs an `MLflow tracking server` with:
  - `PostgreSQL` as `metadata backend`
  - `MinIO` as `artifact store` (S3-compatible)
  - a job container for automatic `MinIO` bucket creation
Configuration values are loaded from `.env`


#### Run

```bash
docker compose up -d

# Check that MLflow and MinIO ports are correctly mapped
docker compose port mlflow 5000     # expected: 0.0.0.0:5000
docker compose port minio 9001      # expected: 0.0.0.0:9001

# Quick health checks
curl -I http://127.0.0.1:5000/      # expect: 200
curl -I http://127.0.0.1:9001/      # expect: 200

# Check running containers
docker compose ps

# Open in browser:
# MLflow UI: http://127.0.0.1:5000
# MinIO Console: http://127.0.0.1:9001/
# Credentials (from .env):
# user: minioadmin
# pass: minioadmin

# Stop and remove all containers, networks, and volumes
docker compose down
```