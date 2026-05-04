#!/bin/bash
python fetch_jobs.py
cd job_transform
dbt run --target prod
dbt test --target prod

