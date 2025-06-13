from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import LogConfig

POSTGRES_CONN_ID = 'postgres-datastore'
SOURCE_DATABASE = 'public' # The equivalent of the source/cloud layer of the DCDF framework.
TARGET_DATABASE = 'raw'
DBT_CONTAINER_NAME = 'dbt'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'raw_ingest_intraday',
    default_args=default_args,
    description='Run the first layer of dbt data models',
    schedule='0 0 * * *',
    start_date=datetime(2025, 6, 12),
    catchup=False,
    tags=["acura","raw","ingest","intraday"]
)

source_layer_dq_check = EmptyOperator(
    task_id='source_layer_dq_check',
    dag=dag   
)

dbt_run_raw_layer = BashOperator(
    task_id='dbt_run_raw_layer',
    bash_command=f"""
        set -e
        # Connect to virtual host machine unix sock
        export DOCKER_HOST=tcp://docker-service-proxy:2375

        # Stop and remove this containerized task in case it still exists
        docker stop dbt && docker rm -f dockertask__dbt_run_raw_layer || true

        # Run the dbt command in an ephemeral container
        docker run --rm \
                -i \
                --name dockertask__dbt_run_raw_layer \
                -e PGPASSWORD=password \
                -e PGUSER=acura_user \
                -e PGHOST=postgres-datastore \
                -e PGPORT=5432 \
                -e PGDATABASE=acura_db \
                -v ${{AIRFLOW_PROJ_DIR}}/dbt_logic:/usr/app/dbt/ \
                --network acura_backend \
                --platform linux/amd64 \
                ghcr.io/dbt-labs/dbt-postgres:1.9.latest \
                run --profiles-dir /usr/app/dbt/profiles --full-refresh --log-level info""",
    do_xcom_push=False,
    dag=dag
)

start = EmptyOperator(
    task_id='start',
    dag=dag
)

end = EmptyOperator(
    task_id='end',
    dag=dag
)

start >> source_layer_dq_check >> dbt_run_raw_layer >> end
