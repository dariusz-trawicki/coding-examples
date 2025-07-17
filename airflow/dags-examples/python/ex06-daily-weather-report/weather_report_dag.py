import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append("/home/airflow/.local/lib/python3.12/site-packages")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from weather_utils import fetch_weather_data, generate_report_pdf

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
}

def generate_pdf_task():
    data = fetch_weather_data()
    generate_report_pdf(data)

with DAG(
    dag_id='ex06_daily_weather_report',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=["example", "weather", "pdf"],
    description="Fetches weather data and generates a daily PDF report"
) as dag:

    fetch_data = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather_data,
    )

    generate_pdf = PythonOperator(
        task_id='generate_weather_pdf',
        python_callable=generate_pdf_task,
    )

    fetch_data >> generate_pdf
