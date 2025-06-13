# docker/airflow-worker/Dockerfile

# Base Airflow image from your docker-compose.yml
# This should match your AIRFLOW_IMAGE_NAME or the default (apache/airflow:3.0.2)
# Make sure to update this if you change your AIRFLOW_IMAGE_NAME
FROM apache/airflow:3.0.2

# Switch to root user to install packages
USER root

# Install dependencies for curl and ca-certificates (needed for downloading the plugin)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* # Clean up apt cache

# Install Docker Compose CLI plugin
# Get the latest stable version from https://github.com/docker/compose/releases
# As of current date (June 2025), v2.27.1 is a recent stable version.
# Check for a newer stable version if available.
ARG DOCKER_COMPOSE_VERSION=v2.27.1
ARG DOCKER_CLI_PLUGINS_DIR=/usr/local/lib/docker/cli-plugins # Standard path for plugins

# Create the plugin directory and download the binary
RUN mkdir -p ${DOCKER_CLI_PLUGINS_DIR} && \
    curl -SL https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64 -o ${DOCKER_CLI_PLUGINS_DIR}/docker-compose && \
    chmod +x ${DOCKER_CLI_PLUGINS_DIR}/docker-compose

# Ensure the plugin directory is in the PATH for the 'airflow' user
# This might already be covered by default PATH, but explicitly adding for clarity.
ENV PATH="${PATH}:${DOCKER_CLI_PLUGINS_DIR}"

# Switch back to the Airflow user
USER airflow

# Set your working directory for DAGs and other Airflow components
WORKDIR /opt/airflow/dags

# Copy your DAGs into the container (assuming your DAGs are in ./airflow/dags on the host)
# This uses the same path as your volume mount in docker-compose.yml
COPY ./airflow/dags /opt/airflow/dags/

# Copy your dbt_logic into the container
# Assuming your dbt_logic is a sibling to your 'airflow' directory on the host:
# e.g., your_project/
#        ├── airflow/
#        ├── dbt_logic/
#        └── docker-compose.yml
# And you want it mounted at /opt/airflow/dags/dbt_logic inside the worker.
# Adjust the source path (./dbt_logic) if it's in a different location relative to this Dockerfile.
COPY ./dbt_logic /opt/airflow/dags/dbt_logic/

# If you have custom Python dependencies specific to your worker (e.g., dbt-core, psycopg2)
# Create a requirements.txt in your docker/airflow-worker/ directory:
# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt