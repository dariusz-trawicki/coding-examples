from airflow.decorators import dag, task

# import from include/dataset.py 
from include.datasets import DATASET_COCKTAIL

@task(outlets=[DATASET_COCKTAIL])
def get_cocktail():
    import requests
    api = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    response = requests.get(api)
    with open(DATASET_COCKTAIL.uri, "wb") as f:
        f.write(response.content)
    return len(response.content)

@task
def check_size(request_size: int):
    print(f"Response size: {request_size} bytes")