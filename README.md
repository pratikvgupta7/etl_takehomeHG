This project implements a containerized ELT data pipeline that ingests customer churn data, transforms it using dbt, and orchestrates the workflow using Prefect.
The system is designed to be easy to run locally, fully open-source, and modular, enabling the pipeline to be extended for production environments.


Architecture
The pipeline follows a modern ELT architecture:
CSV → Python → Postgres (Raw/Staging Tables) → dbt → Analytics Tables → Metabase Dashboards
Workflow orchestration and scheduling are handled by Prefect.


Components
Data Source
Customer churn dataset:
https://www.kaggle.com/datasets/abdullah0a/telecom-customer-churn-insights-for-analysis



Postgres
Acts as the data warehouse storing:
raw.customer_churn_raw — ingested data
staging.stg_churn — cleaned and standardized data
production.churn_report — aggregated reporting tables



Python Ingestion Layer
app/ingest.py
Responsibilities:
Load CSV dataset
Standardize column names
Insert rows into Postgres raw table
Track ingestion timestamp



dbt Transformation Layer
dbt is used to:
- clean missing values
- standardize schema
- anonymize PII
- create reporting models
Example transformations include:
- null value handling
- type casting
- business aggregations
Models:
dbt_project/models/staging/stg_churn.sql
dbt_project/models/marts/churn_report.sql



Prefect orchestrates the pipeline execution.
The workflow is defined in:
- orchestration/flow.py
Pipeline tasks:
ingest -> dbt run -> dbt test
Each step includes:
- retry policies
- logging
- dependency ordering
Prefect provides:
- workflow scheduling
- execution tracking
- retries
- pipeline observability


Scheduling
The pipeline is deployed using Prefect Serve and runs automatically via cron scheduling.
Example schedule:
0 * * * *
Meaning:
Pipeline runs every hour
Schedules can be viewed in the Prefect dashboard.
Prefect UI:
http://localhost:4200





----------------------------------------------------------Running the Pipeline-------------------------------------------------------
1. Clone repository
****git clone <repo>**
**cd etl_takehomeHG****
2. Start infrastructure
**docker compose up -d postgres metabase prefect-server**
3. Start the Prefect pipeline runner
**docker compose up -d prefect**
The runner registers the deployment and begins listening for scheduled runs.
4. Open Prefect UI
**http://localhost:4200**
From the dashboard you can:
- view scheduled runs
- trigger manual runs
- monitor logs
- inspect task execution

Running Metabase
Metabase runs at:
**http://localhost:3000**
Connect Metabase to the Postgres database to visualize the reporting tables.
docker compose up

Dashboard
http://localhost:3000
