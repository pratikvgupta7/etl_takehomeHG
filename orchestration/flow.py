import os
os.environ["PREFECT_API_URL"] = "http://prefect-server:4200/api"
#os.environ["PREFECT_SERVER_ALLOW_EPHEMERAL_MODE"] = "false"

from prefect import flow, task
import subprocess


@task(retries=2, retry_delay_seconds=30)
def ingest():
    result = subprocess.run(
        ["python", "/app/ingest.py"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("Ingestion failed")


@task(retries=2, retry_delay_seconds=30)
def dbt_run():
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "/dbt_project", "--profiles-dir", "/dbt_project"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("dbt run failed")


@task(retries=2, retry_delay_seconds=30)
def dbt_test():
    result = subprocess.run(
        ["dbt", "test", "--project-dir", "/dbt_project", "--profiles-dir", "/dbt_project"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("dbt test failed")


@flow(name="customer-churn-elt")
def churn_pipeline():
    ingest()
    dbt_run()
    dbt_test()


if __name__ == "__main__":
    churn_pipeline.serve(
        name="hourly-churn-pipeline",
        cron="0 * * * *"
    )