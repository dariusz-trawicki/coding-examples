from airflow.decorators import dag, task
from pendulum import datetime

# import from include/exporter_tasks.py
from include.extractor_tasks import get_cocktail, check_size 

@dag(
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False
)
def extractor():
    size = get_cocktail()
    check_size(size)

extractor()
