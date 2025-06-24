import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import subprocess

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
    "ex02-copy-webpages-dag",
    default_args=default_args,
    description="A DAG to copy webpages using wget",
    schedule_interval=timedelta(days=1),
    tags=["learn"],
)


def download_webpage(url, output_path):
    print(subprocess.run(["wget", "-O", output_path, url], check=True))
    return True


# Define tasks using the download_webpage function
download_page_1 = PythonOperator(
    task_id="download_page_1",
    python_callable=download_webpage,
    op_args=[
        "https://airflow.apache.org",
        "./example_page1.html",
    ],  # URL and output path
    dag=dag,
)

download_page_2 = PythonOperator(
    task_id="download_page_2",
    python_callable=download_webpage,
    op_args=["https://airflow.apache.org", "./example_page2.html"],
    dag=dag,
)

download_page_3 = PythonOperator(
    task_id="download_page_3",
    python_callable=download_webpage,
    op_args=["https://airflow.apache.org", "./example_page3.html"],
    dag=dag,
)


# Set task dependencies
download_page_1 >> download_page_2 >> download_page_3
