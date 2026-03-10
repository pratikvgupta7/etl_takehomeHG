#!/bin/bash

docker exec ingestion python ingest.py
docker exec dbt dbt run