import os
from datetime import timedelta
from airflow.models import Variable
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

model_path = Variable.get("MODEL")
with DAG(
        "airflow-inherence",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(0),
) as dag:
    inference = DockerOperator(
        image="airflow-work",
        command="/data/raw/{{ ds }}/data.csv /data/predictions/{{ ds }}/predictions.csv "+f"{model_path}",
        network_mode="bridge",
        task_id="docker-airflow-work",
        do_xcom_push=False,
        mount_tmp_dir=False,
       mounts=[Mount(source=r"C:\Users\mnker\Desktop\airflow-examples-main\data", target="/data", type='bind')]
    )
    
    inference
