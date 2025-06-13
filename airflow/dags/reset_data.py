from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator # type: ignore
from airflow.operators.empty import EmptyOperator # type: ignore
from datetime import datetime

POSTGRES_CONN_ID = 'postgres-datastore'
TARGET_DATABASE = 'public' # The equivalent of the source/cloud layer of the DCDF framework.

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'reset_data',
    default_args=default_args,
    schedule='0 0 * * *',
    tags=["acura","reset"]
)

# Credit Card comparison information source table

drop_cc_comp_info_source_table = SQLExecuteQueryOperator(
    task_id='drop_cc_comp_info_source_table',
    sql= f"""DROP TABLE IF EXISTS {TARGET_DATABASE}.cc_comp_info CASCADE;""",
    conn_id=POSTGRES_CONN_ID,
    show_return_value_in_logs=True,
    dag=dag
)

create_cc_comp_info_source_table = SQLExecuteQueryOperator(
    task_id='create_cc_comp_info_source_table',
    sql=f""" CREATE TABLE {TARGET_DATABASE}.cc_comp_info (
                card_name VARCHAR(255),
                annual_fee VARCHAR(255),
                card_type VARCHAR(255),
                recommended_credit_score VARCHAR(255),
                intro_apr_rate FLOAT,
                intro_apr_duration VARCHAR(255),
                ongoing_apr_fixed FLOAT,
                ongoing_apr_variable FLOAT,
                foreign_transaction_fee FLOAT
        );""",
    conn_id=POSTGRES_CONN_ID,
    show_return_value_in_logs=True,
    dag=dag
)

insert_data_cc_comp_info_source_table = SQLExecuteQueryOperator(
    task_id='insert_data_cc_comp_info_source_table',
    sql=f"""COPY {TARGET_DATABASE}.cc_comp_info(card_name, annual_fee, card_type, recommended_credit_score, intro_apr_rate, intro_apr_duration, ongoing_apr_fixed, ongoing_apr_variable, foreign_transaction_fee)
           FROM '/var/lib/postgresql/mock_data/credit_cards_comparison.csv'
           DELIMITER ','
           CSV HEADER;""",
    conn_id=POSTGRES_CONN_ID,
    show_return_value_in_logs=True,
    dag=dag
)

# Credit Card user review information source table

drop_cc_review_events_source_table = SQLExecuteQueryOperator(
    task_id='drop_cc_review_events_source_table',
    sql= f"""DROP TABLE IF EXISTS {TARGET_DATABASE}.cc_review_events CASCADE;""",
    conn_id=POSTGRES_CONN_ID,
    show_return_value_in_logs=True,
    dag=dag
)

create_cc_review_events_source_table = SQLExecuteQueryOperator(
    task_id='create_cc_review_events_source_table',
    sql=f"""
        CREATE TABLE {TARGET_DATABASE}.cc_review_events (
            card_name VARCHAR(255),
            platform_name VARCHAR(255),
            review_timestamp TIMESTAMP,
            review_id VARCHAR(255),
            review_customer_id VARCHAR(255),
            review_customer_name VARCHAR(255),
            review_rating_maximum NUMERIC(1,0),
            review_rating_given NUMERIC(1,0),
            review_raw_text VARCHAR(255)
        );""",
    conn_id=POSTGRES_CONN_ID,
    show_return_value_in_logs=True,
    dag=dag
)

insert_data_cc_review_events_source_table = SQLExecuteQueryOperator(
    task_id='insert_data_cc_review_events_source_table',
    sql=f"""COPY {TARGET_DATABASE}.cc_review_events(card_name, platform_name, review_timestamp, review_id, review_customer_id, review_customer_name, review_rating_maximum, review_rating_given, review_raw_text)
           FROM '/var/lib/postgresql/mock_data/credit_cards_reviews.csv'
           DELIMITER ','
           CSV HEADER;""",
    conn_id=POSTGRES_CONN_ID,
    show_return_value_in_logs=True,
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

drop_ok = EmptyOperator(
    task_id='drop_ok',
    dag=dag   
)

create_ok = EmptyOperator(
    task_id='create_ok',
    dag=dag   
)

start >> [drop_cc_comp_info_source_table, drop_cc_review_events_source_table] >> drop_ok \
      >> [create_cc_comp_info_source_table, create_cc_review_events_source_table] >> create_ok \
      >> [insert_data_cc_comp_info_source_table, insert_data_cc_review_events_source_table] >> end
