from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, duration

@dag(start_date=datetime(2025, 6 ,1),
     schedule='@weekly',
     catchup=True,
     description="Example DAG",
     tags=["team_a", "do_nothing_dag"],
     default_args={"retries": 1},
     dagrun_timeout=duration(minutes=20),
     max_consecutive_failed_dag_runs=2)
def do_nothing_dag():
    
    # Task example - do nothing
    ta = EmptyOperator(task_id='ta')
    
do_nothing_dag()

