# What does this DAG do?
# It runs pg_dump on the "Airflow DB" once a day and saves the 
# dump to /tmp inside the Airflow worker.


import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

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
    "bash04-pg-dump",
    default_args=default_args,
    description="bash04: pg_dump",
    schedule_interval=timedelta(days=1),
    tags=["learn", "bash"],
)

date_task = BashOperator(
    task_id="date_task",
    bash_command="PGPASSWORD='airflow' pg_dump --host=postgres --username=airflow --dbname=airflow > /tmp/$(date '+%Y-%m-%d___%H-%M-%S')-data.dump",
    dag=dag,
)

date_task
