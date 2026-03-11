FROM python:3.10-slim

WORKDIR /workspace

COPY orchestration/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY orchestration /workspace/orchestration
COPY app /workspace/app
COPY dbt_project /workspace/dbt_project

CMD ["python", "/workspace/orchestration/flow.py"]