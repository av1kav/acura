# acura
A containerized user review analytics platform that uses publicly available information about card products to guide feature roadmap planning and identify key areas of focus for business development. Use the environment setup command below to automatically configure and launch all the necessary services:

``docker-compose -f docker-compose.yml -f airflow/docker-compose.airflow.yml up -d``

## Components

### Database: Postgres

#### RDBMS service
Configured in `docker-compose.yml` under the service name `postgres-datastore`. To reset the database to its initial (mock data) state, use:

``docker exec -i postgres-datastore psql -U acura_user -d acura_db -f /docker-entrypoint-initdb.d/setup.sql``

You should see output like:

```
    BEGIN
    DROP TABLE
    CREATE TABLE
    COMMIT
    BEGIN
    COPY 6
    COMMIT
```

#### Adminer GUI
The adminer service runs on `0.0.0.0:8086`.

![alt text](assets/adminer.png)

The username and password are present in the `profiles.yml` configuration file under `dbt_logic/`.

### Orchestration: Airflow
Airflow services are configured together in a `docker-compose.airflow.yml` file under `airflow/` directory. This configuration is then merged with the main `docker-compose.yml` at execution time of the `docker-compose up` command (see top section of this readme).

![alt text](assets/airflow.png)

The Airflow webserver runs on `0.0.0.0:8080`. The username and password are present in the `airflow/docker-compose.airflow.yml` file. 

### Data Transformations: dbt

The dbt service is configured as a container bridged into the same network shared by the remaining services. Data architecture is designed according to the Snowflake Data Cloud Deployment Framework (DCDF) and has the following layers:

1. Source/Cloud: `public` schema
2. Raw layer: `raw` schema
3. Integration layer: `integration` schema
4. Presentation layer: `presentation` schema
5. Share layer: `share` schema

![alt text](assets/dcdf.png)

Though the Source and Cloud layers are usually not part of Snwflake (and in this case, Postgres), this project assumes the containers are running as cloud services/microservices and so there is no additional ingress; source data in the `public` schema is referenced by dbt models starting from the `raw` layer.


Please note that due to dbt naming conventions, the prefix `public_` will be attached to all dbt models, due to the configuration of only a development dbt profile. So, for example, the `raw` schema would appear as `public_raw`.

### Data Quality: deequ
### Analytics: pySpark
### Exploration: jupyter-pyspark
A jupyterlab instance with fully a configured Spark environment is available on a URL in the logs of the `jupyter-pyspark` container:

![alt text](assets/jupyter-pyspark.png)

### Dashboarding: Tableau(??)

## Containerization using Docker
### Network (`docker network ls`)
All container services are bound to the same network named `backend`, which resolves to `acura-backend` due to the project name. These services include:
- Postgres: the main Postgres service, adminer
- Airflow: workers, webserver, internal postgres db, internal redis db
- dbt: all transformation operations on the Postgres db

## Source Data
Currently, only mock data is used to simulate real-world collected data.