from airflow.decorators import dag, task
from datetime import datetime
from airflow.datasets import Dataset
import os
import re

file_path = "/usr/local/airflow/dags/shared_file.csv"
my_file = Dataset(file_path)

@dag(start_date=datetime(2023, 1, 1), schedule="@daily", catchup=False)
def dag_a():
    @task(outlets=[my_file])
    def write_file():
        current_value = 0

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
                match = re.search(r"New DATA\s*-\s*(\d+)", content)
                if match:
                    current_value = int(match.group(1))

        next_value = current_value + 1

        with open(file_path, "w") as f:
            f.write(f"New DATA - {next_value}\n")

    write_file()

dag_a = dag_a()
