## Transaction Fraud Detection Demo (Rule-Based System)

### Overview
This project simulates a **credit card fraud detection system** using a **rule-based engine**.  
It generates synthetic banking transactions, evaluates them against predefined rules, and stores the results in a **PostgreSQL** database.  

The setup can be monitored with **Prometheus** and **Grafana**, allowing you to visualize real-time transaction patterns, fraud decisions, and database metrics.

---

### Key Components

| Component | Description |
|------------|-------------|
| **PostgreSQL** | Stores generated transaction records and rule evaluation results |
| **Python + Faker** | Generates random synthetic transaction data |
| **Rule Engine (`run_rules`)** | Applies simple fraud detection rules to each transaction |
| **Prometheus** | Scrapes PostgreSQL metrics through `postgres_exporter` |
| **Grafana** | Visualizes database performance and fraud statistics |

---

### Logic: Rule-Based Fraud Detection

The system applies a few simple rules to simulate fraud detection:

| Rule ID | Condition | Decision | Explanation |
|----------|------------|-----------|--------------|
| **Rule1** | Real-time transaction **≥ $100** and **account not blacklisted** |  Rejected | “Transaction amount ≥ $100 in real-time” |
| **Rule2** | Account **blacklisted** and **real-time transaction** | Rejected | “Blacklisted account/card” |
| — | Any non-real-time transaction | Approved | Not subject to fraud checks |
| — | Default (no rule triggered) | Approved | No risk identified |

> 💡 *“Real-time transaction”* means a typical card payment at a store (POS or online).  
> Other types such as *disputes* or *settlements* are treated as non-real-time.

---

### Table Schema (`banking_data`)

| Column | Type | Description |
|---------|------|-------------|
| `id` | SERIAL | Primary key |
| `timestamp` | TIMESTAMPTZ | Transaction timestamp |
| `uniq_id` | UUID | Unique transaction ID |
| `trans_type` | VARCHAR | Transaction type (`Real_time_transaction`, `dispute`, `settlement`) |
| `amount` | DECIMAL | Transaction amount |
| `amount_crr` | DECIMAL | Converted amount |
| `account_holder_name` | VARCHAR | Customer name |
| `card_presense` | VARCHAR | Whether the card was physically present |
| `merchant_category` | VARCHAR | Merchant category (e.g. Grocery, Electronics) |
| `card_type` | VARCHAR | Visa / Mastercard |
| `card_id` | VARCHAR | Last 4 digits of the card number |
| `account_id` | UUID | Unique customer account ID |
| `account_blacklisted` | BOOLEAN | True if account is blacklisted |
| `rules_triggered` | VARCHAR | Which rule was triggered |
| `rules_explanation` | VARCHAR | Description of the rule |
| `decision` | VARCHAR | Final system decision (`Approved` / `Rejected`) |

---

### How It Works

1. **Table Creation** – The script ensures the `banking_data` table exists.
2. **Record Generation** – Each record is created using the `Faker` library.
3. **Rule Evaluation** – The record is passed to the `run_rules()` function.
4. **Database Insert** – Transaction and decision are inserted into PostgreSQL.
5. **Monitoring** – Prometheus and Grafana visualize the metrics.

---

### Running the Demo

#### 1. Provision PostgreSQL with Terraform (AWS RDS)

```bash
cd terraform
terraform init
terraform apply
# Example output:
# db_instance_endpoint = "mltestdb-instance.c34keo06inrq.eu-central-1.rds.amazonaws.com:5432"

# Test the connection:
psql "host=mltestdb-instance.c34keo06inrq.eu-central-1.rds.amazonaws.com port=5432 dbname=mltestdb user=postgres password='postgres' sslmode=require"
# mltestdb=>
# mltestdb-> \q   # exit
```

#### 2. Generate Example Data (Python Script)

Create a new Conda virtual environment and install project dependencies:

```bash
# Create env
cd ..
conda create -p ./venv python=3.10 -y
conda activate ./venv
pip install -r requirements.txt
```

If needed, install Jupyter to run the notebook interactively:

```bash
pip install jupyter
```

In `app.ipynb`, set the RDS endpoint, for example:

```python
DB_HOST = "mltestdb-instance.c34keo06inrq.eu-central-1.rds.amazonaws.com"
```

Then run the notebook:

```bash
jupyter notebook app.ipynb
```

### Monitoring — Prometheus & Grafana

In the `monitoring/docker-compose.yml`, update the RDS endpoint for the `postgres_exporter` service:

```yaml
environment:
  DATA_SOURCE_NAME: >-
    postgresql://postgres:postgres@mltestdb-instance.c34keo06inrq.eu-central-1.rds.amazonaws.com:5432/postgres?sslmode=require
```

Then start the monitoring stack:
```bash
cd monitoring
docker compose up -d
```

---

### Access the Monitoring Dashboards

Once all containers are up, open the following URLs in your browser:

| Service | URL | Default Credentials |
|----------|-----|---------------------|
| **Grafana UI** | [http://localhost:3000](http://localhost:3000) | **admin / admin** |
| **Prometheus UI** | [http://localhost:9090](http://localhost:9090) | *(no login required)* |

---

### Inside Grafana

1. Log in to Grafana (`http://localhost:3000`).  
2. Open the preloaded dashboard: **PostgreSQL Overview**.  
3. You’ll see real-time metrics such as:
   - Exporter up  
   - Connections (total)  
   - Transactions per second (TPS)  
   - Rollbacks per second  

NOTE: Dashboard files and provisioning are preconfigured in `grafana/provisioning` and `grafana/dashboards`.


### CLEAN UP

```bash
cd ..
conda deactivate
conda remove -p ./venv --all

cd terraform
terraform destroy

cd ../monitoring
docker compose down
```