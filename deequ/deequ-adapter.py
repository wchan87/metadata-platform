from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from py4j.java_collections import JavaClass
from pyspark.context import SparkContext
from pyspark.sql import DataFrame, SparkSession

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
    dyf.show()
    return dyf

def write_output_dq_results(glue_context: GlueContext, dq_results: DynamicFrame) -> None:
    glue_context.write_dynamic_frame.from_options(
        frame=dq_results,
        connection_type="file",
        connection_options={"path": "/home/hadoop/workspace/temp/output/RCCCBBALTOT/"},
        format="parquet"
    )

def evaluate_dq_via_deequ(spark_context: SparkContext, dyf: DynamicFrame, ruleset: str) -> DynamicFrame:
    java_class: JavaClass = spark_context._jvm.com.amazon.deequ.dqdl.EvaluateDataQuality
    # https://github.com/awslabs/deequ/blob/master/src/main/scala/com/amazon/deequ/dqdl/EvaluateDataQuality.scala
    result_df_java: DataFrame = java_class.process(dyf.toDF()._jdf, ruleset)
    result_df_python: DataFrame = DataFrame(result_df_java, dyf.glue_ctx.spark_session)
    result_df_python.show()
    return DynamicFrame.fromDF(result_df_python, dyf.glue_ctx, "dq_results")

def main():
    spark_context: SparkContext = SparkContext.getOrCreate()
    glue_context: GlueContext =  GlueContext(spark_context)
    dyf: DynamicFrame = load_input_data(glue_context)
    ruleset: str = "Rules = [ColumnExists \"observation_date\", IsComplete \"observation_date\"]"
    dyf_dq_results: DynamicFrame = evaluate_dq_via_deequ(spark_context, dyf, ruleset)
    write_output_dq_results(glue_context, dyf_dq_results)

if __name__ == "__main__":
    main()
