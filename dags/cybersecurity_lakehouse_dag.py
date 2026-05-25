from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "Shweta",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="cybersecurity_lakehouse_pipeline",
    description="Cybersecurity lakehouse pipeline using PySpark, MinIO and Airflow",
    default_args=default_args,
    start_date=datetime(2026, 5, 21),
    schedule="@daily",
    catchup=False
) as dag:
    generate_logs = BashOperator(
        task_id="generate_secuirty_logs",
        bash_command="cd /opt/airflow && python scripts/generate_logs.py "
    )
    bronze_ingestion = BashOperator(
        task_id="bronze_ingestion",
        bash_command="cd /opt/airflow && python spark_jobs/bronze_ingestion.py "
    )
    silver_cleaning = BashOperator(
        task_id="silver_cleaning",
        bash_command="cd /opt/airflow && python spark_jobs/silver_cleaning.py "
    )
    gold_analytics = BashOperator(
        task_id="gold_analytics",
        bash_command="cd /opt/airflow && python spark_jobs/gold_analytics.py "
    )
    upload_to_minio = BashOperator(
        task_id="upload_to_minio",
        bash_command="cd /opt/airflow && python spark_jobs/upload_to_minio.py "
    )
generate_logs >> bronze_ingestion >> silver_cleaning >> gold_analytics >> upload_to_minio