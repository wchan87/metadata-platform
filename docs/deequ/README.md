# Deequ

[Deequ](#java-api) with its Python API, [python-deequ](#python-api) is built on top of Apache Spark by Amazon and used internally as per the [AWS Big Data Blog > Test data quality at scale with Deequ](https://aws.amazon.com/blogs/big-data/test-data-quality-at-scale-with-deequ/). [AWS Glue Data Quality](#aws-glue-data-quality) was rolled out in 2023 for wider usage by teams already using AWS Glue.

## Java API

See [deequ](https://github.com/awslabs/deequ) for the source code.

## Python API

See [python-deequ](https://github.com/awslabs/python-deequ) for the source code and [documentation](https://pydeequ.readthedocs.io/en/latest/README.html).

```bash
pip install pydeequ
```

## AWS Glue Data Quality

See [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html) for documentation on usage of AWS Glue Data Quality.

[DockerHub > amazon/aws-glue-libs](https://hub.docker.com/r/amazon/aws-glue-libs) doesn't have the AWS Glue Data Quality as per [limitations highlighted](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html#develop-local-docker-considerations)
```bash
docker pull amazon/aws-glue-libs:5
```
