import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

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
    "shape-04-1-211-212-221-222-3",
    default_args=default_args,
    description="shape 04 1-211-212-221-222-3",
    schedule_interval=timedelta(days=1),
    tags=["learn", "shape"],
)


def function1():
    print("function1")
    return True


task_1 = PythonOperator(
    task_id="task-1",
    python_callable=function1,
    dag=dag,
)

task_2_1_1 = PythonOperator(
    task_id="task-2-1-1-id",
    python_callable=function1,
    dag=dag,
)

task_2_1_2 = PythonOperator(
    task_id="task-2-1-2-id",
    python_callable=function1,
    dag=dag,
)

task_2_2_1 = PythonOperator(
    task_id="task-2-2-1-id",
    python_callable=function1,
    dag=dag,
)

task_2_2_2 = PythonOperator(
    task_id="task-2-2-2-id",
    python_callable=function1,
    dag=dag,
)

task_3 = PythonOperator(
    task_id="task-3-id",
    python_callable=function1,
    dag=dag,
)
# DAG strukture
#         1
#        / \
#   2-1-1  2-2-1
#    |      |
#   2-1-2  2-2-2
#        \ /
#         3

task_1 >> [task_2_1_1, task_2_2_1]
task_2_1_1 >> task_2_1_2 >> task_3
task_2_2_1 >> task_2_2_2 >> task_3
