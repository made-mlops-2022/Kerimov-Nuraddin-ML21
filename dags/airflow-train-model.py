import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount
from airflow.sensors.external_task_sensor import ExternalTaskSensor

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "catchup": False,
    "retry_delay": timedelta(seconds=5),
}

with DAG(
        "airflow-train-model",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(0),
) as dag:
    wait_for_data =ExternalTaskSensor(
        task_id='wait_for_data',
        external_dag_id='airflow-get-data',
        external_task_id='docker-airflow-get-data',
        execution_delta = timedelta(minutes=10),
        timeout=300,
        dag=dag)
    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="/data/raw/{{ ds }} data.csv target.csv /data/processed/{{ ds }} data.csv",
        network_mode="bridge",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
       mounts=[Mount(source=r"C:\Users\mnker\Desktop\airflow-examples-main\data", target="/data", type='bind')]
    )
    test_train_split = DockerOperator(
        image="airflow-test_train_split",
        command="/data/processed/{{ ds }} data.csv train.csv val.csv",
        network_mode="bridge",
        task_id="docker-airflow-train-test-split",
        do_xcom_push=False,
        mount_tmp_dir=False,
       mounts=[Mount(source=r"C:\Users\mnker\Desktop\airflow-examples-main\data", target="/data", type='bind')]
    )

    train_model = DockerOperator(
        image="airflow-train-model",
        command="/data/processed/{{ ds }} train.csv /data/model model.pkl ",
        network_mode="bridge",
        task_id="docker-airflow-train-model",
        do_xcom_push=False,
        mount_tmp_dir=False,
       mounts=[Mount(source=r"C:\Users\mnker\Desktop\airflow-examples-main\data", target="/data", type='bind')]
    )
    validate_model = DockerOperator(
        image="airflow-validate-model",
        command="/data/processed/{{ ds }} val.csv /data/model model.pkl ",
        network_mode="bridge",
        task_id="docker-airflow-validate-model",
        do_xcom_push=False,
        mount_tmp_dir=False,
       mounts=[Mount(source=r"C:\Users\mnker\Desktop\airflow-examples-main\data", target="/data", type='bind')]
    )
    wait_for_data >> preprocess >> test_train_split >> train_model >> validate_model
