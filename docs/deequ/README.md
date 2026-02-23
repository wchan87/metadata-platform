# Deequ

[Deequ](#java-api) with its Python API, [python-deequ](#python-api) is built on top of Apache Spark by Amazon and used internally as per the [AWS Big Data Blog > Test data quality at scale with Deequ](https://aws.amazon.com/blogs/big-data/test-data-quality-at-scale-with-deequ/). [AWS Glue Data Quality](#aws-glue-data-quality) was rolled out in 2023 for wider usage by teams already using AWS Glue.

## Data Quality Definition Language

"[Data Quality Definition Language (DQDL)](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html) is a domain specific language that you use to define rules for AWS Glue Data Quality."

## Java API

See [deequ](https://github.com/awslabs/deequ) for the source code.

## Python API

See [python-deequ](https://github.com/awslabs/python-deequ) for the source code and [documentation](https://pydeequ.readthedocs.io/en/latest/README.html).

```bash
pip install pydeequ
```

## AWS Glue Data Quality

See [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html) for documentation on the usage of AWS Glue Data Quality.

[DockerHub > amazon/aws-glue-libs](https://hub.docker.com/r/amazon/aws-glue-libs) doesn't have the AWS Glue Data Quality as per [limitations highlighted](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html#develop-local-docker-considerations) so a wrapper that mimics the `awsgluedq` module may be needed to allow AWS Glue job to [check data quality](https://aws.amazon.com/blogs/big-data/enable-strategic-data-quality-management-with-aws-glue-dqdl-labels/) as well.
1. Pull the AWS Glue Docker image
    ```bash
    docker pull amazon/aws-glue-libs:5.0.8
    ```
2. Implement the Glue job, [glue-dq.py](/deequ/glue-dq.py) with the following considerations to [run](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html#develop-local-docker-image-setup-run) via Docker
   1. Create a wrapper that mimics what AWS does via [awsgluedq.transforms.EvaluateDataQuality](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-transforms-EvaluateDataQuality.html)
      * Note that `awsgluedq` could be subject to a dependency confusion attempt, see [PEP 541 Request: awsgluedq #5610](https://github.com/pypi/support/issues/5610) so be wary about importing it.
   2. Switch directory to the workspace
      ```bash
      cd deequ
      ```
   3. Setup environment variables
      ```bash
      export MSYS_NO_PATHCONV=1
      export WORKSPACE_LOCATION=$PWD
      export SCRIPT_FILE_NAME=glue-dq.py
      ```
   4. Download the [RCCCBBALTOT.csv](https://fred.stlouisfed.org/series/RCCCBBALTOT) file to [deequ/temp](/deequ/temp) folder
   5. Execute the Glue job via [spark-submit](https://spark.apache.org/docs/latest/submitting-applications.html)
      ```bash
       docker run -it --rm \
          -v $WORKSPACE_LOCATION:/home/hadoop/workspace/ \
          --name glue5_spark_submit \
          amazon/aws-glue-libs:5.0.8 \
          -c "pip3 install pydeequ==1.4.0 && spark-submit --packages com.amazon.deequ:deequ:2.0.13-spark-3.5 /home/hadoop/workspace/$SCRIPT_FILE_NAME"
       ```
      * `--packages` will automatically download the Java dependencies necessary for this to run
