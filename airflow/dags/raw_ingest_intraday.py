from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

POSTGRES_CONN_ID = 'postgres-datastore'
SOURCE_DATABASE = 'public' # The equivalent of the source/cloud layer of the DCDF framework.
TARGET_DATABASE = 'raw'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
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
    task_id='drop_ok',
    dag=dag   
)

dbt_run_raw_layer = BashOperator(
    task_id='dbt_run_raw_layer',
    bash_command="docker exec dbt-container dbt run --project-dir /opt/dbt/project",
    dag=dag
)

dbt_run_raw_layer_test = BashOperator(
    task_id='dbt_test',
    bash_command="docker exec dbt-container dbt run --project-dir /opt/dbt/project",
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

start >> source_layer_dq_check >> dbt_run_raw_layer >> dbt_run_raw_layer_test >> end
