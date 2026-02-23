from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
import os
from pyspark.context import SparkContext
from pyspark.sql import DataFrame, SparkSession

# necessary to ensure the relevant variable is set for pydeequ to work
os.environ['SPARK_VERSION'] = '3.5'

def load_input_data(glue_context: GlueContext) -> DynamicFrame:
    dyf: DynamicFrame = glue_context.create_dynamic_frame.from_options(
        connection_type="file",
        connection_options={"paths": ["/home/hadoop/workspace/temp/input/RCCCBBALTOT.csv"]},
        format="csv",
        format_options={
            "withHeader": True,
            "delimiter": ","
        },
        transformation_ctx="dyf_from_s3"
    )
    dyf.printSchema()
    return dyf

def write_output_dq_results(glue_context: GlueContext, dq_results: DynamicFrame) -> None:
    glue_context.write_dynamic_frame.from_options(
        frame=dq_results,
        connection_type="file",
        connection_options={"path": "/home/hadoop/workspace/temp/output/RCCCBBALTOT/"},
        format="parquet"
    )

# doesn't work without AWS Glue itself and for reference
# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-transforms-EvaluateDataQuality.html
def evaluate_dq_via_awsgluedq(ruleset: str, dyf: DynamicFrame) -> DynamicFrame:
    from awsgluedq.transforms import EvaluateDataQuality
    dyf_dq_results: DynamicFrame  = EvaluateDataQuality.apply(
        frame=dyf,
        ruleset=ruleset,
        publishing_options={
            "dataQualityEvaluationContext": "dyf",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True,
            "resultsS3Prefix": "amzn-s3-demo-bucket1",
        },
    )
    dyf_dq_results.printSchema()
    dyf_dq_results.toDF().show()
    return dyf_dq_results

# https://blog.dataengineerthings.org/pydeequ-tutorial-practical-data-quality-checks-for-healthcare-dataset-886d0fc8be7b
def evaluate_dq_via_pydeequ(dyf: DynamicFrame) -> DynamicFrame:
    from pydeequ.checks import Check, CheckLevel, CheckResult
    from pydeequ.verification import VerificationSuite, VerificationResult
    spark_session = dyf.glue_ctx.spark_session
    # https://pydeequ.readthedocs.io/en/latest/pydeequ.html#module-pydeequ.checks
    check: Check = Check(spark_session, CheckLevel.Error, "Data Quality Checks")
    check_result: CheckResult = VerificationSuite(spark_session) \
        .onData(dyf.toDF()) \
        .addCheck(check.hasSize(lambda x: x == 53)) \
        .run()
    df_dq_results: DataFrame = VerificationResult.checkResultsAsDataFrame(spark_session, check_result)
    return DynamicFrame.fromDF(df_dq_results, dyf.glue_ctx, "dyf_dq_results")

# necessary to ensure that PyDeequ is properly released as per https://pydeequ.readthedocs.io/en/latest/README.html#wrapping-up
def shutdown(glue_context: GlueContext) -> None:
    spark_session: SparkSession = glue_context.spark_session
    spark_session.sparkContext._gateway.shutdown_callback_server()
    spark_session.stop()

def main():
    spark_context: SparkContext = SparkContext.getOrCreate()
    # https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html
    glue_context: GlueContext =  GlueContext(spark_context)
    # https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html
    dyf: DynamicFrame = load_input_data(glue_context)
    ruleset: str = """Rules = [ColumnExists "observation_date", IsComplete "observation_date"]"""
    # dyf_dq_results: DynamicFrame = evaluate_dq_via_awsgluedq(ruleset, dyf)
    dyf_dq_results: DynamicFrame = evaluate_dq_via_pydeequ(dyf)
    write_output_dq_results(glue_context, dyf_dq_results)
    shutdown(glue_context)

if __name__ == "__main__":
    main()
