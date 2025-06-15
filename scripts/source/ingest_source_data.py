import psycopg2
import requests
import sys
import yaml
import io
import csv
import pandas as pd
import numpy as np

# Expect first arg to be abspath to this script
sources_config_filepath = sys.argv[1]
if not sources_config_filepath:
    print('No sources.yml argument provided as cmdline args; defaulting to scripts/source')
    sources_config_filepath ='/opt/airflow/scripts/source/sources.yml'
sources_config = yaml.safe_load(open(sources_config_filepath))

# Iteratively drop/create/load configured sources
for source in sources_config:
    desc = source['desc']
    source_type = source['source_type']
    url = source['url']
    schema = source['schema']
    table_name = source['table_name']
    table_drop_sql = source['table_drop_sql']
    table_create_sql = source['table_create_sql']

    # Fetch step
    print(f"FETCH: {desc}")
    response = requests.get(url)
    data = response.json()['hits']['hits']
    df = pd.json_normalize(data, sep='_')
    df.replace({np.nan: None}, inplace=True)
    print(df.head())

    buffer = io.StringIO()
    df.to_csv(buffer, sep='|', index=False, quoting=csv.QUOTE_ALL)

    with psycopg2.connect(
        dbname='acura_db',
        user='acura_user',
        password='password',
        host='postgres-datastore',
        port=5432
    ) as conn:
        cur = conn.cursor()

        # Recreate table step
        print(f"RECREATE: {desc}")
        cur.execute(table_drop_sql.format(schema=schema, table_name=table_name))
        cur.execute(table_create_sql.format(schema=schema, table_name=table_name))
        conn.commit()

        # Load Table step
        print(f"LOAD: {desc}")
        buffer.seek(0)
        cur.copy_expert(f"COPY {schema}.{table_name} FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER '|', QUOTE '\"')", buffer)
        print(f"Loaded {len(df)} row(s) into {schema}.{table_name}")
        conn.commit()