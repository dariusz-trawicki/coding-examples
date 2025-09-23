import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import os
import requests
from google.cloud import storage
from google.oauth2 import service_account


BUCKET_NAME = "xxxxx-bucket-name"
# Path to your service account key file
SERVICE_ACCOUNT_KEY_FILE_PATH = (
    "/opt/airflow/airflow-ac-key.json"  # in container (for: local airflow in docker)
)
# File path in the GCP bucket
GCP_FILE_PATH = "airflow/data/planets-3.json"
# The URL to fetch data from
URL = "https://swapi.dev/api/planets/3"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(0),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

dag = DAG(
    "starwars-to-gcp-bucket-DAG",
    default_args=default_args,
    description="A DAG to download data and save it to files",
    schedule_interval=timedelta(days=1),
    tags=["learn"],
)


def download_data_to_bucket(
    url, service_account_key_file_path, bucket_name, gcp_file_path
):
    # --- Help code
    pwd = os.getcwd()
    print(f"pwd return: '{pwd}'")  # in container -> path: /opt/airflow
    ls_output = os.popen("ls").read()
    print(f"ls return:'{ls_output}'")
    # ---

    # Initialize the GCP client
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key_file_path
    )
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcp_file_path)

    # Fetch data from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Save data to the GCP bucket
        blob.upload_from_string(response.text)
        print(f"File saved to GCP bucket {bucket_name} at {gcp_file_path}")
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
    return True


download_planets_to_bucket_task = PythonOperator(
    task_id="download_planets_to_bucket",
    python_callable=download_data_to_bucket,
    op_args=[URL, SERVICE_ACCOUNT_KEY_FILE_PATH, BUCKET_NAME, GCP_FILE_PATH],
    dag=dag,
)

download_planets_to_bucket_task
