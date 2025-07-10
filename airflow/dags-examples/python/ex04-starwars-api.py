import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import os
import requests

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
    "ex04-starwars-api-DAG",
    default_args=default_args,
    description="A DAG to download data and save it to files",
    schedule_interval=timedelta(days=1),
    tags=["learn"],
)


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
    return True


def download_data(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "w") as f:
            f.write(response.text)
        print(f"Data from {url} saved to {file_path}.")
    else:
        print(
            f"Failed to download data from {url}. Status code: {response.status_code}"
        )
    return True


create_folder_task = PythonOperator(
    task_id="create_folder",
    python_callable=create_folder,
    op_args=["/tmp/airflow-data"],
    dag=dag,
)

download_people_task = PythonOperator(
    task_id="download_people",
    python_callable=download_data,
    op_args=["https://swapi.dev/api/people/1", "/tmp/airflow-data/people-1.json"],
    dag=dag,
)

download_starships_task = PythonOperator(
    task_id="download_starships",
    python_callable=download_data,
    op_args=["https://swapi.dev/api/starships/9", "/tmp/airflow-data/starships-9.json"],
    dag=dag,
)

download_planets_task = PythonOperator(
    task_id="download_planets",
    python_callable=download_data,
    op_args=["https://swapi.dev/api/planets/3", "/tmp/airflow-data/planets-3.json"],
    dag=dag,
)

create_folder_task >> [
    download_people_task,
    download_starships_task,
    download_planets_task,
]
