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
    "shape-03-1-3-1-3-1",
    default_args=default_args,
    description="shape 03 1-3-1-3-1",
    schedule_interval=timedelta(days=1),
    tags=["learn", "shape"],
)


def function1():
    print("function1")
    return True


task_1 = PythonOperator(
    task_id="task-1-id",
    python_callable=function1,
    dag=dag,
)

task_2_a = PythonOperator(
    task_id="task-2-a-id",
    python_callable=function1,
    dag=dag,
)

task_2_b = PythonOperator(
    task_id="task-2-b-id",
    python_callable=function1,
    dag=dag,
)

task_2_c = PythonOperator(
    task_id="task-2-c-id",
    python_callable=function1,
    dag=dag,
)

task_3 = PythonOperator(
    task_id="task-3-id",
    python_callable=function1,
    dag=dag,
)

task_4_a = PythonOperator(
    task_id="task-4-a-id",
    python_callable=function1,
    dag=dag,
)

task_4_b = PythonOperator(
    task_id="task-4-b-id",
    python_callable=function1,
    dag=dag,
)

task_4_c = PythonOperator(
    task_id="task-4-c-id",
    python_callable=function1,
    dag=dag,
)

task_5 = PythonOperator(
    task_id="task-5-id",
    python_callable=function1,
    dag=dag,
)


(
    task_1
    >> [task_2_a, task_2_b, task_2_c]
    >> task_3
    >> [task_4_a, task_4_b, task_4_c]
    >> task_5
)
