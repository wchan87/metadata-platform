# Open Metadata

[Open Metadata](https://open-metadata.org/) which seems to be a competing standard with Egeria. There's a connector to support integration with [OpenLineage](../openlineage/README.md). Open Metadata seems to be associated with a [startup](https://www.crunchbase.com/organization/collate), [Collate](https://www.getcollate.io/about) that has some key data engineering folks in their senior leadership team.

## Local Setup

Based on [Open Metadata > Deployment > Docker Deployment](https://docs.open-metadata.org/latest/deployment/docker), the following steps should give you the full cluster locally.
1. Create and switch directory
    ```bash
    mkdir openmetadata-docker && cd openmetadata-docker
    ```
2. Download as `docker-compose.yml` and make some modifications to add [MySQL](https://hub.docker.com/_/mysql/), [ElasticSearch](https://hub.docker.com/_/elasticsearch/) and [Airflow](https://hub.docker.com/r/apache/airflow) (specifically combining the [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml) with the one from Open Metadata) containers
    ```bash
    curl -L -o docker-compose.yml https://github.com/open-metadata/OpenMetadata/releases/download/1.10.1-release/docker-compose-openmetadata.yml
    ```
3. Setup Docker Compose cluster
    ```bash
    docker compose up -d
    ```
   * http://localhost:8585/ - `admin@open-metadata.org` / `admin` is the default credentials
4. Administer Docker Compose cluster
   * Stop the Docker Compose cluster
       ```bash
       docker compose stop
       ```
   * Teardown the Docker Compose cluster
       ```bash
       docker compose down --volumes
       ```
