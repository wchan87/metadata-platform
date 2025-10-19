# Metadata Platform Exploration

The summarized table below is derived from Copilot Deep Research assessment of websites related to the metadata products

| Standard | Data Lineage | Metadata Management | Integration Capabilities | Ecosystem Support | Adoption Level | Organization Backing |
| -- | -- | -- | -- | -- | -- | -- |
| [Egeria](docs/egeria/README.md) | Advanced, auto & manual (graph, impact analysis, OpenLineage integration) | Comprehensive, 800+ types, governance as code | Extensive connectors (databases, Kafka, Atlas, Unity Catalog, REST APIs) | IBM, ODPI, Linux Foundation, open community | High in complex/enterprise settings | IBM, Linux Foundation |
| [Open Data Contract Standard](docs/odcs/README.md) | Lineage via RDF, enforceable contracts | YAML-based, versioned, testable rules | CLI, dbt, API, Excel, CI/CD, Data Mesh Manager | Bitol, Linux Foundation, open-source | Growing in data mesh/data contract orgs | [Bitol](https://bitol.io/), [Linux Foundation](https://www.linuxfoundation.org/projects) |
| [Open Data Product Specification](docs/odps/README.md) | Embedded via ODCS/refs, SLA & DQ tiers | Modular, AI-ready, 120+ metadata attributes | Stripe, SodaCL, data lakes, APIs, DCAT ext., marketplaces | Linux Foundation, FIWARE, NATO, BASF | Accelerating (gov, enterprise, marketplace) | Linux Foundation, distributed |
| [OpenLineage](docs/openlineage/README.md) | Granular, event-based, standardized API, column-level | Focus on lineage facets, not general metadata | Integrations with Airflow, dbt, Spark, Flink, Snowflake | Linux Foundation, Marquez, Astronomer, Atlan | Explosive in lineage-driven orgs | Linux Foundation, Astronomer |
| [Open Metadata](docs/openmetadata/README.md) | Column/table-level, ingest & manual editing, dbt/Lineage API | Unified, extensible model, versioning, rich governance | 50+ connectors, REST, Python SDK, Great Expectations, Amundsen | Collate, Atlan, strong open-source | Rapid, across digital/data-first orgs | [Collate](https://www.getcollate.io/), Atlan, community |
