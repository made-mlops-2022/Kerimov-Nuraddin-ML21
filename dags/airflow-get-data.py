import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "catchup": False,
    "retry_delay": timedelta(seconds=5),
}

with DAG(
        "airflow-get-data",
        default_args=default_args,
        schedule_interval="*/5 * * * *",
        start_date=days_ago(0),
) as dag:
    get_data = DockerOperator(
        image="airflow-get-data",
        command="/data/raw/{{ ds }} data.csv target.csv",
        network_mode="bridge",
        task_id="docker-airflow-get-data",
        do_xcom_push=False,
        mount_tmp_dir=False,
       mounts=[Mount(source=r"C:\Users\mnker\Desktop\airflow-examples-main\data", target="/data", type='bind')]
    )
    get_data
