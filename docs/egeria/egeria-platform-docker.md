# Egeria Platform via Docker

## Pragmatic Data Research - Getting Started

There is an additional getting started guide by Pragmatic Data Research consultancy via [Getting Started with Egeria](https://getting-started-with-egeria.pdr-associates.com/introduction.html). The distribution that's precompiled appears to be based on the [OMAG Server Platform](https://github.com/odpi/egeria) repository which in turn appears to be packaged as Docker image, [odpi/egeria-platform](https://hub.docker.com/r/odpi/egeria-platform). Note that the `platforms` directory referenced in the guide appears to refer to `/deployments` directory within the container.

1. Pull the latest stable version
    ```bash
    docker pull odpi/egeria-platform:5.3
    ```
2. Run the container and bind to port 9443
    ```bash
    docker run -p 9443:9443 --name egeria-platform -d odpi/egeria-platform:5.3
    ```
    * https://localhost:9443/ depends on Kafka to initialize properly so some additional work is needed to assess how to approach this
    * https://localhost:9443/swagger-ui/index.html for OpenAPI specification

## Docker Compose Cluster

An alternative approach is through the [odpi/egeria-workspaces](https://github.com/odpi/egeria-workspaces) which leverages Docker Compose to ensure all the related containers are set up.

1. Clone the repository. An error occurs which needs to be handled later.
    ```bash
    git clone git@github.com:odpi/egeria-workspaces.git
    ```
    ```
    Cloning into 'egeria-workspaces'...
    remote: Enumerating objects: 9025, done.
    remote: Counting objects: 100% (152/152), done.
    remote: Compressing objects: 100% (123/123), done.
    remote: Total 9025 (delta 33), reused 67 (delta 18), pack-reused 8873 (from 1)
    Receiving objects: 100% (9025/9025), 268.55 MiB | 13.47 MiB/s, done.
    Resolving deltas: 100% (3779/3779), done.
    error: invalid path 'exchange/Obsidian/Templates/Digital Product Manager/Link_Agreement->Item.md'
    fatal: unable to checkout working tree
    warning: Clone succeeded, but checkout failed.
    You can inspect what was checked out with 'git status'
    and retry with 'git restore --source=HEAD :/'
    ```
2. Switch directory
    ```bash
    cd egeria-workspaces
    ```
3. Switch to `wsl`, use `git reset --hard` and exit to resolve the error.
    ```bash
    wsl
    git reset --hard
    exit
    ```
4. Switch directory to one of the example Docker Compose configuration
    ```bash
    cd compose-configs/egeria-quickstart
    ```
5. Remove `restart: always` from `services.postgres` to prevent it from automatically restarting with Docker Desktop
6. Run `docker compose` to start the containers
    ```bash
    docker compose -f egeria-quickstart.yaml up --build -d
    ```
    * Jupyter: http://localhost:7888 (use `egeria` as password)
7. Use `docker compose` to interact with the containers
    * Start the cluster
        ```bash
        docker compose -f egeria-quickstart.yaml up -d
        ```
    * Stop the cluster
        ```bash
        docker compose -f egeria-quickstart.yaml stop
        ```
    * Stop the cluster
        ```bash
        docker compose -f egeria-quickstart.yaml down --volumes
        ```
