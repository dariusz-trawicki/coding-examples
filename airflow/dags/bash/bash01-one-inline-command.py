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
    "bash01-one-inline-command",
    default_args=default_args,
    description="bash01: one inline command",
    schedule_interval=timedelta(days=1),
    tags=["learn", "bash"],
)


date_task = BashOperator(
    task_id="date_task",
    bash_command="date && hostname && pwd",
    dag=dag,
)

date_task
