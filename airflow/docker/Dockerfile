FROM apache/airflow:3.0.2

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* # Clean up apt cache

ARG DOCKER_COMPOSE_VERSION=v2.27.1
ARG DOCKER_CLI_PLUGINS_DIR=/usr/local/lib/docker/cli-plugins

RUN mkdir -p ${DOCKER_CLI_PLUGINS_DIR} && \
    curl -SL https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64 -o ${DOCKER_CLI_PLUGINS_DIR}/docker-compose && \
    chmod +x ${DOCKER_CLI_PLUGINS_DIR}/docker-compose

ENV PATH="${PATH}:${DOCKER_CLI_PLUGINS_DIR}"

USER airflow

WORKDIR /opt/airflow/dags

# Move DAGs
COPY ./airflow/dags /opt/airflow/dags/

# Move dbt logic
COPY ./dbt_logic /opt/airflow/dags/dbt_logic/

# Install requirements.txt on workers
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt