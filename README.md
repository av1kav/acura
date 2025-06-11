# acura
A containerized user review analytics platform that uses publicly available information about card products to guide feature roadmap planning and identify key areas of focus for business development. Use the environment setup command below to automatically configure and launch all the necessary services:

``docker-compose -f docker-compose.yml -f airflow/docker-compose.airflow.yml up -d``

## Components

### Database: Postgres
Configured in `docker-compose.yml` under the service name `postgres`. To reset the database to its initial (mock data) state, use:

``docker exec -i postgres-datastore psql -U acura_user -d acura_db -f /docker-entrypoint-initdb.d/setup.sql``

You should see output like

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
The adminer service runs on `0.0.0.0:8086`. The username and password are present in the `profiles.yml` configuration file under `dbt_logic/`.

### Orchestration: Airflow
Configured in its own `docker-compose.airflow.yml` file under `airflow/` directory. Merged with the main `docker-compose.yml` at execution time of the `docker-compose up` command (see top section of this readme).

The Airflow webserver runs on `0.0.0.0:8080`. The username and password are present in the `airflow/docker-compose.airflow.yml` file. 

### Data Transformations: dbt

The dbt service is configured as a container bridged into the same network shared by the remaining services.

### Data Quality: deequ
### Analytics: pySpark
### Dashboarding: Tableau(??)

## Containerization using Docker
### Network (`docker network ls`)
All container services are bound to the same network named `backend`, which resolves to `acura-backend` due to the project name. These services include:
- Postgres: the main Postgres service, adminer
- Airflow: workers, webserver, internal postgres db, internal redis db
- dbt: all transformation operations on the Postgres db

## Source Data
Currently, only mock data is used to simulate real-world collected data.