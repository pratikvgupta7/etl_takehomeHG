import os
os.environ["PREFECT_API_URL"] = "http://prefect-server:4200/api"
#os.environ["PREFECT_SERVER_ALLOW_EPHEMERAL_MODE"] = "false"

from prefect import flow, task
import subprocess
from prefect import get_run_logger

@task(retries=2, retry_delay_seconds=30)
def ingest():
    logger = get_run_logger()

    result = subprocess.run(
        ["python", "ingest.py"],
        cwd="/workspace/app",
        capture_output=True,
        text=True,
    )

    logger.info("STDOUT:\n%s", result.stdout)
    logger.info("STDERR:\n%s", result.stderr)
    logger.info("Return code: %s", result.returncode)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)


@task(retries=2, retry_delay_seconds=30)
def dbt_run():
    logger = get_run_logger()
    result = subprocess.run(
        ["dbt", "run"],
        cwd="/workspace/dbt_project",
        env=os.environ,
        capture_output=True,
        text=True,
    )

    logger.info(result.stdout)

    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(result.stderr)


@task(retries=2, retry_delay_seconds=30)
def dbt_test():
    logger = get_run_logger()

    result = subprocess.run(
        ["dbt", "test"],
        cwd="/workspace/dbt_project",
        env=os.environ,
        capture_output=True,
        text=True,
    )

    logger.info(result.stdout)

    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(result.stderr)


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