from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from airflow.operators.empty import EmptyOperator # type: ignore
from datetime import datetime

POSTGRES_CONN_ID = 'postgres-datastore'
DBT_CONTAINER_NAME = 'dbt'
DBT_LOG_LEVEL = 'info'

def create_dbt_exec_operator(task_id, dbt_command):
    """
    Return a BashOperator configured to run DBT transformations.
    
    Args:
        task_id (str): The name of the task_id for this BashOperator
        dbt_command (str): The command to run on the dbt container. This string must NOT
            start with 'dbt'. So, to configure an operator to run `dbt run --full-refresh`,
            simply provide `run --full-refresh`.
    """
    return BashOperator(
        task_id=task_id,
        bash_command=f"""
            set -e
            # Connect to virtual host machine unix sock
            export DOCKER_HOST=tcp://docker-service-proxy:2375

            # Stop and remove this containerized task in case it still exists
            docker stop dbt && docker rm -f dockertask__dbt_run_raw_layer || true

            # Run the dbt command in an ephemeral container
            docker run --rm \
                    -i \
                    --name dockertask__{task_id} \
                    -e PGPASSWORD=password \
                    -e PGUSER=acura_user \
                    -e PGHOST=postgres-datastore \
                    -e PGPORT=5432 \
                    -e PGDATABASE=acura_db \
                    -v ${{AIRFLOW_PROJ_DIR}}/dbt_logic:/usr/app/dbt/ \
                    --network acura_backend \
                    --platform linux/amd64 \
                    ghcr.io/dbt-labs/dbt-postgres:1.9.latest \
                    {dbt_command} --log-level {DBT_LOG_LEVEL}""",
        do_xcom_push=False,
        dag=dag
    )

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
    description='Run the raw layer of Acura dbt data models',
    schedule='0 0 * * *',
    start_date=datetime(2025, 6, 12),
    catchup=False,
    tags=["acura","raw","ingest","intraday"]
)

dbt_run_raw_layer = create_dbt_exec_operator(
    task_id='dbt_run_raw_layer',
    dbt_command = 'run --profiles-dir /usr/app/dbt/profiles --select raw.*'
)

dbt_test_raw_layer = create_dbt_exec_operator(
    task_id='dbt_test_raw_layer',
    dbt_command = 'test --profiles-dir /usr/app/dbt/profiles --select raw.*'
)

start = EmptyOperator(
    task_id='start',
    dag=dag
)

end = EmptyOperator(
    task_id='end',
    dag=dag
)

start >> dbt_run_raw_layer >> dbt_test_raw_layer >> end
