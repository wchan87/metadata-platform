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
     * Register for an account. Note the email address is irrelevant but is used to login since the MailDog SMTP test server is used for testing purposes.
       * User: `admin`
       * Password: `entropydata`
     * Create an organization called [FRED](#fred-organization-setup)
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
## FRED Organization Setup

To simulate an organization, we will use [Federal Reserve Economic Data](https://fred.stlouisfed.org/) to try the Entropy Data UI:
1. Create the data domains on http://localhost:8081/fred/domains based on [FRED > Categories](https://fred.stlouisfed.org/categories)
   * [Money, Banking, & Finance](https://fred.stlouisfed.org/categories/32991) - `money-banking-finance`
     * [Financial Indicators](https://fred.stlouisfed.org/categories/46) - `financial-indicators`
     * [Banking](https://fred.stlouisfed.org/categories/23) - `banking`
       * [Consumer Credit](https://fred.stlouisfed.org/categories/101) - `consumer-credit`
2. Create the data products on http://localhost:8081/fred/dataproducts based on the individual data sets that were analyzed
    * [RCCCBBALTOT](https://fred.stlouisfed.org/series/RCCCBBALTOT)
    * [RCCCBBALREV](https://fred.stlouisfed.org/series/RCCCBBALREV)
3. Create the data contracts on http://localhost:8081/fred/studio/datacontracts
4. Create the business definitions on http://localhost:8081/fred/studio/definitions
