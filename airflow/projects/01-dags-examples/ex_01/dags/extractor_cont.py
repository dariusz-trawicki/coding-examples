from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, duration

# import from include/dataset.py 
from include.datasets import DATASET_COCKTAIL

@dag(start_date=datetime(2025, 1 ,1),
     schedule=[DATASET_COCKTAIL],
     catchup=True,
     description="This DAG processes ...",
     tags=["team_a", "extractor_cont"],
     default_args={"retries": 1},
     dagrun_timeout=duration(minutes=20),
     max_consecutive_failed_dag_runs=2)
def extractor_cont():

    ta = EmptyOperator(task_id='ta')
    
extractor_cont()

