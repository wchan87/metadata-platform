# Entropy Data

Refer to [Docker Compose instructions](https://docs.entropy-data.com/installation-docker) with [docker-compose.yml](/entropy-data/docker-compose.yml) modified to not automatically start up with Docker
1. Change directory to [entropy-data](/entropy-data)
    ```bash
    cd entropy-data
    ```
2. Set up the Docker Compose cluster
    ```bash
    docker compose up -d
    ```
   * Access the Entropy Data UI at http://localhost:8081
   * Access the MailDog SMTP test server at http://localhost:8025
3. Administer Docker Compose cluster
   * Stop the Docker Compose cluster
       ```bash
       docker compose stop
       ```
   * Tear down the Docker Compose cluster
       ```bash
       docker compose down --volumes
       ```
