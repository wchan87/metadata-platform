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

See [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html) for documentation on the usage of AWS Glue Data Quality.

[DockerHub > amazon/aws-glue-libs](https://hub.docker.com/r/amazon/aws-glue-libs) doesn't have the AWS Glue Data Quality as per [limitations highlighted](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html#develop-local-docker-considerations) so we must mimic the `awsgluedq` module to allow the AWS Glue job to [check data quality](https://aws.amazon.com/blogs/big-data/enable-strategic-data-quality-management-with-aws-glue-dqdl-labels/).

Note that `awsgluedq` could be subject to a dependency confusion attempt, see [PEP 541 Request: awsgluedq #5610](https://github.com/pypi/support/issues/5610) so be wary about importing it.

There are two options to mimic `awsgluedq` module, specifically [awsgluedq.transforms.EvaluateDataQuality](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-transforms-EvaluateDataQuality.html):
* wrapper around [pydeequ](#python-api)
* wrapper around [deequ](#java-api)

Both options have been implemented:
1. Pull the AWS Glue Docker image
    ```bash
    docker pull amazon/aws-glue-libs:5.0.8
    ```
2. Switch directory to the workspace
    ```bash
    cd deequ
    ```
3. Setup environment variables
    ```bash
    export MSYS_NO_PATHCONV=1
    export WORKSPACE_LOCATION=$PWD
    ```
4. Download the [RCCCBBALTOT.csv](https://fred.stlouisfed.org/series/RCCCBBALTOT) file to the [deequ/temp](/deequ/temp) folder
5. Run the [pydeequ-adapter.py](/deequ/pydeequ-adapter.py)
   1. Setup environment variables
      ```bash
      export SCRIPT_FILE_NAME=pydeequ-adapter.py
      ```
   2. Execute the Glue job via [spark-submit](https://spark.apache.org/docs/latest/submitting-applications.html)
      ```bash
       docker run -it --rm \
          -v $WORKSPACE_LOCATION:/home/hadoop/workspace/ \
          --name glue5_spark_submit \
          amazon/aws-glue-libs:5.0.8 \
          -c "pip3 install pydeequ==1.4.0 && spark-submit --packages com.amazon.deequ:deequ:2.0.13-spark-3.5 /home/hadoop/workspace/$SCRIPT_FILE_NAME"
       ```
      * `--packages` will automatically download the Java dependencies necessary for this to run
6. Run the [deequ-adapter.py](/deequ/deequ-adapter.py)
   1. Setup environment variables
      ```bash
      export SCRIPT_FILE_NAME=deequ-adapter.py
      ```
   2. Execute the Glue job via [spark-submit](https://spark.apache.org/docs/latest/submitting-applications.html)
      ```bash
       docker run -it --rm \
          -v $WORKSPACE_LOCATION:/home/hadoop/workspace/ \
          --name glue5_spark_submit \
          amazon/aws-glue-libs:5.0.8 \
          spark-submit --packages com.amazon.deequ:deequ:2.0.13-spark-3.5,software.amazon.glue:dqdl:1.0.0 /home/hadoop/workspace/$SCRIPT_FILE_NAME
       ```
      * `--packages` will automatically download the Java dependencies necessary for this to run

### Usage Details

Note that `awsglue.data_quality` may either be an early internal import path that AWS uses or a hallucination that persisted in LLMs. For the sake of consistency with AWS documentation, we will assume that `awsgluedq.transforms` is the intended import path. There's a possibility that the similarly named [EvaluateDataQuality.scala](https://github.com/awslabs/deequ/blob/master/src/main/scala/com/amazon/deequ/dqdl/EvaluateDataQuality.scala) in deequ may be the origin of some hallucinations.

[awsgluedq.transforms.EvaluateDataQuality.apply](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-transforms-EvaluateDataQuality.html#aws-glue-api-crawler-pyspark-transforms-EvaluateDataQuality-apply) - inherits [awsglue.transforms.GlueTransform.apply](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-transforms-GlueTransform.html#aws-glue-api-crawler-pyspark-transforms-GlueTransform-apply) method on the base class
* Arguments
  * `frame` - an instance of [awsglue.dynamicframe.DynamicFrame](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
  * `ruleset` - string representation of the ruleset defined based on [DQDL](#data-quality-definition-language)
  * `publishing_options`
    * `dataQualityEvaluationContext` - appears to be a string representation of the variable name for the output
    * `enableDataQualityCloudWatchMetrics`
    * `enableDataQualityResultsPublishing`
    * `resultsS3Prefix`
* Return
  * Appears to be an instance of [awsglue.dynamicframe.DynamicFrame](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)

`awsgluedq.transforms.EvaluateDataQuality.process_rows` - There is no official documentation of this function, but it's covered in tutorials on the AWS Glue Studio (especially [notebooks](https://docs.aws.amazon.com/glue/latest/dg/data-quality-gs-studio-notebooks.html))
* Arguments
  * `input` - an instance of [awsglue.dynamicframe.DynamicFrame](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
  * `ruleset` - string representation of the ruleset defined based on [DQDL](#data-quality-definition-language)
  * `publishing_options`
    * `dataQualityEvaluationContext` - appears to be a string representation of the variable name for the output
    * `enableDataQualityCloudWatchMetrics`
    * `enableDataQualityResultsPublishing`
  * `additional_options`
    * `performanceTuning.caching`
    * `publishAggregatedMetrics.status` - "You may require [aggregated metrics](https://docs.aws.amazon.com/glue/latest/dg/tutorial-data-quality.html#data-quality-aggregated-metrics) such as number of records that passed, failed, skipped at a rule level or at the ruleset level to build dashboards."
* Return
  * `EvaluateDataQualityMultiframe` - There is no official documentation of this class, but it is referenced by AWS Glue Studio tutorials and AWS Glue Web API as a [data type](https://docs.aws.amazon.com/glue/latest/webapi/API_EvaluateDataQualityMultiFrame.html).

### Data Quality Definition Language

"[Data Quality Definition Language (DQDL)](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html) is a domain specific language that you use to define rules for AWS Glue Data Quality."

> ## DQDL syntax
> A DQDL document is case sensitive and contains a ruleset, which groups individual data quality rules together. To construct a ruleset, you must create a list named Rules (capitalized), delimited by a pair of square brackets. The list should contain one or more comma-separated DQDL rules like the following example.
> 
> ```
> Rules = [
>   IsComplete "order-id",
>   IsUnique "order-id"
> ]
> ```
> 
> ### Rule structure
> The structure of a DQDL rule depends on the rule type. However, DQDL rules generally fit the following format.
> ```
> <RuleType> <Parameter> <Parameter> <Expression>
> ```
> RuleType is the case-sensitive name of the rule type that you want to configure. For example, IsComplete, IsUnique, or CustomSql. Rule parameters differ for each rule type. For a complete reference of DQDL rule types and their parameters, see DQDL rule type reference.

The following section will be an attempt to map the concepts of DQDL to its underlying deequ concepts.

| DQDL Rule Type  | PyDeequ Core API | Deequ Check |
| -- | -- | - |
| [AggregateMatch](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-AggregateMatch.html) | | |
| [ColumnCorrelation](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnCorrelation.html) | Check.hasCorrelation | Check.hasCorrelation |
| [ColumnCount](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnCount.html) | | Check.hasColumnCount |
| [ColumnDataType](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnDataType.html) | Check.hasDataType | Check.hasDataType |
| [ColumnExists](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnExists.html) | | Check.hasColumn |
| [ColumnLength](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnLength.html) | Check.hasMinLength <br/> Check.hasMaxLength | Check.hasMinLength <br/> Check.hasMaxLength |
| [ColumnNamesMatchPattern](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnNamesMatchPattern.html) | | |
| [ColumnValues](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ColumnValues.html) | | |
| [Completeness](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-Completeness.html) | | |
| [CustomSQL](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-CustomSQL.html) | | Check.customSql |
| [DataFreshness](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-DataFreshness.html) | | |
| [DatasetMatch](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-DatasetMatch.html) | | Check.doesDatasetMatch |
| [DistinctValuesCount](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-DistinctValuesCount.html) | Check.hasNumberOfDistinctValues | Check.hasNumberOfDistinctValues |
| [Entropy](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-Entropy.html) | Check.hasEntropy | Check.hasEntropy |
| [IsComplete](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-IsComplete.html) | Check.isComplete | Check.isComplete |
| [IsPrimaryKey](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-IsPrimaryKey.html) | Check.isPrimaryKey | Check.isPrimaryKey |
| [IsUnique](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-IsUnique.html) | Check.isUnique | Check.isUnique |
| [Mean](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-Mean.html) | Check.hasMean | Check.hasMean |
| [ReferentialIntegrity](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-ReferentialIntegrity.html) | | |
| [RowCount](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-RowCount.html) | Check.hasSize | Check.hasSize |
| [RowCountMatch](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-RowCountMatch.html) | | |
| [StandardDeviation](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-StandardDeviation.html) | | |
| [Sum](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-Sum.html) | Check.hasSum | Check.hasSum |
| [SchemaMatch](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-SchemaMatch.html) | | |
| [Uniqueness](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-Uniqueness.html) | Check.hasUniqueness | Check.hasUniqueness |
| [UniqueValueRatio](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-UniqueValueRatio.html) | Check.hasUniqueValueRatio | Check.hasUniqueValueRatio |
| [DetectAnomalies](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-DetectAnomalies.html) | | |
| [FileFreshness](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-FileFreshness.html) | | |
| [FileMatch](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-FileMatch.html) | | |
| [FileUniqueness](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-FileUniqueness.html) | | |
| [FileSize](https://docs.aws.amazon.com/glue/latest/dg/dqdl-rule-types-FileSize.html) | | |

Java/Scala (Deequ) Equivalent
* [com.amazon.deequ.checks.Check](https://github.com/awslabs/deequ/blob/master/src/main/scala/com/amazon/deequ/checks/Check.scala)
* [com.amazon.deequ.dqdl.model.ExecutableRule](https://github.com/awslabs/deequ/blob/master/src/main/scala/com/amazon/deequ/dqdl/model/ExecutableRule.scala)
* [com.amazon.deequ.dqdl.translation.rules](https://github.com/awslabs/deequ/tree/master/src/main/scala/com/amazon/deequ/dqdl/translation/rules)

Python (PyDeequ) Equivalent
* [pydeequ.checks.Check](https://pydeequ.readthedocs.io/en/latest/pydeequ.html#pydeequ.checks.Check)
* [pydeequ.analyzers](https://pydeequ.readthedocs.io/en/latest/pydeequ.html#module-pydeequ.analyzers)
