from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'teodora',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='job_scout_orchestrator',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    task_fetch = BashOperator(
        task_id='fetch_jobs',
        bash_command='python3 /opt/airflow/job_scout_code/fetch_jobs.py'
    )

    task_dbt = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/job_scout_code/job_transform && dbt run --profiles-dir . --target prod')

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/job_scout_code/job_transform && dbt test --profiles-dir . --target prod'
    )

    task_notify_success = BashOperator(
        task_id='notify_discord_success',
        bash_command='python3 /opt/airflow/job_scout_code/notifier.py'
    )

    task_fetch >> task_dbt >> dbt_test >> task_notify_success