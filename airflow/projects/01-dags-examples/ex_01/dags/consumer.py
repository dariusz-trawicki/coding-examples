from airflow.decorators import dag, task
from datetime import datetime
from airflow.datasets import Dataset

file_path = "/usr/local/airflow/dags/shared_file.csv"

my_file = Dataset(file_path)

@dag(start_date=datetime(2023, 1, 1), schedule=[my_file], catchup=False)
def dag_b():
    @task
    def process_file():
        with open(file_path, "r") as f:
            data = f.read()
            print(f"New data: {data}")

    process_file()

dag_b = dag_b()
