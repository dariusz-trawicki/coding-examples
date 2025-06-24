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
    "shape-05-a-b-c-d-e-f-g-h-i-j",
    default_args=default_args,
    description="An example DAG",
    schedule_interval=timedelta(days=1),
    tags=["learn", "shape"],
)


def function1():
    print("function1")
    return True


task_A = PythonOperator(
    task_id="task_A",
    python_callable=function1,
    dag=dag,
)

task_B = PythonOperator(
    task_id="task_B",
    python_callable=function1,
    dag=dag,
)

task_C = PythonOperator(
    task_id="task_C",
    python_callable=function1,
    dag=dag,
)

task_D = PythonOperator(
    task_id="task_D",
    python_callable=function1,
    dag=dag,
)

task_E = PythonOperator(
    task_id="task_E",
    python_callable=function1,
    dag=dag,
)

task_F = PythonOperator(
    task_id="task_F",
    python_callable=function1,
    dag=dag,
)

task_G = PythonOperator(
    task_id="task_G",
    python_callable=function1,
    dag=dag,
)

task_H = PythonOperator(
    task_id="task_H",
    python_callable=function1,
    dag=dag,
)

task_I = PythonOperator(
    task_id="task_I",
    python_callable=function1,
    dag=dag,
)

task_J = PythonOperator(
    task_id="task_J",
    python_callable=function1,
    dag=dag,
)

# DAG structure:
#      A
#     / \
#    B   C
#   /|   |\
#  D E   F G
#   \|   |/
#    H   I
#     \ /
#      J

# Define the task dependencies
task_A >> [task_B, task_C]
task_B >> [task_D, task_E]
task_C >> [task_F, task_G]
[task_D, task_E] >> task_H
[task_F, task_G] >> task_I
[task_H, task_I] >> task_J
