import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import subprocess
import os

# name of the folder being created
folder_path_with_name = "./airflow_tasks/download_webpages/folder1"

# the name under which we save the copied webpage
webpage_file_name = "example_page1.html"

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
    "ex03-copy-webpages-into-created-folder-dag",
    default_args=default_args,
    description="A DAG to copy webpages using wget into created folder",
    schedule_interval=timedelta(days=1),
    tags=["learn"],
)


# Create a folder function
def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_path}' created.")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")
    return True


# Download webpage function
def download_webpage(url, output_path):
    # print(folder_path_with_name + '/' + web_file_name)
    print(subprocess.run(["wget", "-O", output_path, url], check=True))
    return True


# Task 1: Create folder
create_folder = PythonOperator(
    task_id="create_folder",
    python_callable=create_folder,
    op_args=[folder_path_with_name],
    dag=dag,
)

# Task 2: Download webpage
download_page = PythonOperator(
    task_id="download_page",
    python_callable=download_webpage,
    op_args=[
        "https://airflow.apache.org",
        folder_path_with_name + "/" + webpage_file_name,
    ],  # URL and output path
    dag=dag,
)

# Set task dependencies
create_folder >> download_page
