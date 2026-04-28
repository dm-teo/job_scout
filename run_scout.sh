#!/bin/bash
venv/bin/python fetch_jobs.py
cd job_transform
../venv/bin/dbt run
../venv/bin/dbt test
sudo -u postgres psql -d job_scout_db -c "SELECT job_title, link FROM analytics.fct_job_leads ORDER BY job_title LIMIT 5;"

