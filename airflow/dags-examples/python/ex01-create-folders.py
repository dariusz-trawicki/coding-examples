import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import os

# Define the default arguments for the DAG
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

# Define the DAG
dag = DAG(
    "ex01-create-folders-dag",
    default_args=default_args,
    description="A simple DAG to create folders",
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=["learn"],
)


# Function to create a folder
def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_path}' created.")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")
    return True


# Task 1: Create folder 1
create_folder_1 = PythonOperator(
    task_id="create_folder_1",
    python_callable=create_folder,
    op_args=["./test-folder1"],
    dag=dag,
)

# Task 2: Create folder 2
create_folder_2 = PythonOperator(
    task_id="create_folder_2",
    python_callable=create_folder,
    op_args=["./test-folder2"],
    dag=dag,
)

# Task 3: Create folder 3
create_folder_3 = PythonOperator(
    task_id="create_folder_3",
    python_callable=create_folder,
    op_args=["./test-folder3"],
    dag=dag,
)

# Set task dependencies
create_folder_1 >> create_folder_2 >> create_folder_3
