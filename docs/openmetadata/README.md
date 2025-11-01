# Open Metadata

[Open Metadata](https://open-metadata.org/) which seems to be a competing standard with Egeria. There's a connector to support integration with [OpenLineage](../openlineage/README.md). Open Metadata seems to be associated with a [startup](https://www.crunchbase.com/organization/collate), [Collate](https://www.getcollate.io/about) that has some key data engineering folks in their senior leadership team.

## Local Setup

Based on [Open Metadata > Deployment > Docker Deployment](https://docs.open-metadata.org/latest/deployment/docker), the following steps should give you the full cluster locally.
1. Create and switch directory
    ```bash
    mkdir openmetadata-docker && cd openmetadata-docker
    ```
2. Download the `docker-compose.yml` from the [releases](https://github.com/open-metadata/OpenMetadata/releases)  (one of the four which has everything needed to run locally) to [openmetadata-docker/docker-compose.yml](../../openmetadata-docker/docker-compose.yml). Remove `restart: always` from the `services` to prevent it from automatically starting at Docker startup. [Kafka](#kafka) was added to the Docker Compose cluster to enable [Open Lineage connector](https://docs.open-metadata.org/latest/connectors/pipeline/openlineage).
    ```bash
    curl -L -o docker-compose.yml https://github.com/open-metadata/OpenMetadata/releases/download/1.10.4-release/docker-compose.yml
    ```
3. Setup Docker Compose cluster
    ```bash
    docker compose up -d
    ```
   * Open Metadata UI - http://localhost:8585/ - user: `admin@open-metadata.org`, password: `admin`
     * MySQL - `jdbc:mysql://localhost:3306/openmetadata_db` - user: `openmetadata_user`, password: `openmetadata_password`, database: `openmetadata_db`
   * Airflow - http://localhost:8080 - user: `admin`, password: `admin`
     * MySQL - `jdbc:mysql://localhost:3306/airflow_db` - user: `airflow_user`, password: `airflow_pass`, database: `airflow_db`
   * ElasticSearch - http://localhost:9200
   * Kafka - `locahost:19092` (from your local machine), `host.docker.internal:9092` (from within any container) or `openmetadata-kafka:9092` (from within container attached to network)
4. Administer Docker Compose cluster
   * Stop the Docker Compose cluster
       ```bash
       docker compose stop
       ```
   * Teardown the Docker Compose cluster
       ```bash
       docker compose down --volumes
       ```

## Kafka

Based on similar instructions for setting up one-node Kafka to facilitate [OpenLineage Connector](#openlineage-connector)
1. Disable Windows path resolution
    ```bash
    export MSYS_NO_PATHCONV=1
    ```
2. Run docker exec to "remote" into the container, alternatively use "Exec" tab on Docker Desktop
    ```bash
    docker exec --workdir /opt/kafka/bin/ -it openmetadata-kafka sh
    ```
3. Create topic to begin pushing events into
    ```bash
    ./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic openlineage-events
    ```

## OpenLineage Connector

From the Open Metadata UI, the parameters that are needed to set up OpenLineage connector are as follows:
* Kafka Brokers List: `openmetadata-kafka:9092`
* Topic Name: `openlineage-events`
* Consumer Group: `openmetadata-openlineage-consumer`

Note that it's still a work-in-progress to figure out how it fits together.
