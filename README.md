# acura
A containerized analytics platform that uses public information to guide feature roadmap planning and identify key areas of focus for business development. Use the environment setup command below to automatically configure and launch all the necessary services

Project environment setup: ``docker-compose -f docker-compose.yml -f airflow/airflow-docker-compose.yml up -d``

## Components

### Database: Postgres
- Configured in `docker-compose.yml` under the service name `postgres`

### Orchestration: Airflow
- Configured in its own `airflow-docker-compose.yml` file under `airflow/` directory. Merged with the main `docker-compose.yml` at execution time of the `docker-compose up` command (see top section of this readme).

### Data Transformations: dbt
### Data Quality: deequ
### Analytics: pySpark
### Dashboarding: Tableau(??)

## Containerization using Docker
