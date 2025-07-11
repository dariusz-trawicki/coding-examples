# Dag examples

## ASTRO CLI - installation

Info: https://www.astronomer.io/docs/astro/cli/overview

```bash
# installation
brew install astro
```

## Run

```bash
# astro dev stop # if needed
astro dev start
```

### First DAG

DAG called `do_nothing_dag` that is:
- Scheduled to `run weekly`
- `Starts` from June 1, 2025
- Will catch up on `missed runs` if Airflow was `down`
- Has default `retry behavior`
- Will `timeout` a DAG run after 20 minutes
- Will `pause` the DAG automatically if it `fails` twice in a row

```bash
# Run dag: ecom 
astro dev run dags test ecom 2025-06-01
```

### DAGs: `dag_a` (`producer`) and `dag_b` (`consumer`)

#### Pipeline

DAG `dag_a` (`producer.py`) runs once per day, and its task:
- Reads a file called `shared_file.csv` (if it exists).
- Extracts the last written number from the line `New DATA - N`.
- Increments that number by 1.
- Writes the updated value back to the same file.
- Publishes the file as a `Dataset`, which can trigger downstream `dag_b` (`consumer.py`).

```bash
# Run dag: dag_a (producer)
astro dev run dags test dag_a  2025-06-01
# *** output ***
# dag_a changes the file shared_file.csv, 
# AND dag_b (consumer) is triggered automatically
```

### Dags: `extractor` and `extractor_cont`

#### Pipeline

 Dag `extractor`:

- Fetches random `cocktail data` from an `external API`.
- Saves it to a local `file` defined as a `Dataset` (`/tmp/cocktail.json`).
- Enables downstream DAG (`extractor_cont`) to be `triggered automatically`  when the data changes.

NOTE: some code is imported from "include" folder.

```bash
# Run extractor dag:
astro dev run dags test extractor  2025-06-01

# TEST
docker ps
# *** output (example) ***
# CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                      NAMES
# 6e5aa4e02340   ex_01_8b9b96/airflow:latest   "tini -- /entrypoint…"   11 minutes ago   Up 11 minutes                              ex_01_8b9b96-scheduler-1
docker exec -it ex_01_8b9b96-scheduler-1 /bin/bash
ls /tmp
# Pretty-prints (formats) the JSON content of cocktail.json file
python -m json.tool /tmp/cocktail.json
```