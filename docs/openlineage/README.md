# OpenLineage

[OpenLineage](https://openlineage.io/) which is backed by many Apache data frameworks and has functionally emerged as the frontrunner in representing data lineage. OpenLineage is part of the Linux Foundation as well.

The [Getting Started](https://openlineage.io/getting-started) guide for OpenLineage suggests [Marquez](https://marquezproject.ai/) as the HTTP backend to collect and visualize OpenLineage events. Refer to [Marquez > Quickstart](https://marquezproject.ai/docs/quickstart/) as well.
* [GitHub > MarquezProject > marquez](https://github.com/MarquezProject/marquez)
  * [openlineage-docker/docker-compose.yml](../../openlineage-docker/docker-compose.yml) is copied from [docker-compose.yml](https://github.com/MarquezProject/marquez/blob/main/docker-compose.yml) with the following modifications
    * Added [docker-compose.web.yml](https://github.com/MarquezProject/marquez/blob/main/docker-compose.web.yml) to ensure the Marquez Web UI is started up as well
    * [openlineage-docker/postgresql.conf](../../openlineage-docker/postgresql.conf) is copied from [postgresql.conf](https://github.com/MarquezProject/marquez/blob/main/docker/postgresql.conf) and mounted to ensure the Postgres container has access to it
    * [openlineage-docker/init-db.sh](../../openlineage-docker/init-db.sh) is copied from [init-db.sh](https://github.com/MarquezProject/marquez/blob/main/docker/init-db.sh) and mounted to ensure the Postgres container is initialized with the account needed by Marquez API container
    * [openlineage-docker/wait-for-it.sh](../../openlineage-docker/wait-for-it.sh) is copied from [wait-for-it.sh](https://github.com/MarquezProject/marquez/blob/main/docker/wait-for-it.sh) and mounted to ensure the Marquez API container can wait before it triggers the `entrypoint.sh`
    * [openlineage-docker/entrypoint.sh](../../openlineage-docker/entrypoint.sh) is copied from [entrypoint.sh](https://github.com/MarquezProject/marquez/blob/main/docker/entrypoint.sh) and mounted to ensure the Marquez API container can start up properly
  * [openlineage-docker/.env](../../openlineage-docker/.env) is copied from [.env.example](https://github.com/MarquezProject/marquez/blob/main/.env.example)
* [DockerHub > marquezproject > marquez](https://hub.docker.com/r/marquezproject/marquez)
* [DockerHub > marquezproject > marquez-web](https://hub.docker.com/r/marquezproject/marquez-web)

1. From the project root directory, switch to specific directory
    ```bash
    cd openlineage-docker
    ```
2. Setup Docker Compose cluster
    ```bash
    docker compose up -d
    ```
   * http://localhost:5000 is where the Marquez API can be accessible from
   * http://localhost:3000 is where the Marquez Web UI can be accessible from
3. Administer Docker Compose cluster
   * Stop the Docker Compose cluster
       ```bash
       docker compose stop
       ```
   * Teardown the Docker Compose cluster
       ```bash
       docker compose down --volumes
       ```
