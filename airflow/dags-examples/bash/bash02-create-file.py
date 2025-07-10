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
    "bash02-create-file",
    default_args=default_args,
    description="bash02: create file",
    schedule_interval=timedelta(days=1),
    tags=["learn", "bash"],
)


date_task = BashOperator(
    task_id="date_task",
    bash_command="date > /tmp/date.txt",
    dag=dag,
)

date_task
