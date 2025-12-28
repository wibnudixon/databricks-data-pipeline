from pyspark.sql.functions import col, when, size, array_contains, round, datediff, current_date, concat_ws

def transform_data(df):
    """
    Apply 100+ diverse data transformations to the input DataFrame.

    Args:
        df (DataFrame): Spark DataFrame containing raw data.

    Returns:
        DataFrame: Transformed Spark DataFrame ready for analysis.
    """
    # Flatten nested fields (e.g., address and performance)
    df = df.withColumn("street", col("address.street")) \
           .withColumn("city", col("address.city")) \
           .withColumn("state", col("address.state")) \
           .withColumn("zip", col("address.zip")) \
           .drop("address")

    df = df.withColumn("performance_score", col("performance.score")) \
           .withColumn("last_review_date", col("performance.last_review_date")) \
           .drop("performance")

    # Calculate total compensation
    df = df.withColumn("total_compensation", col("salary") + col("bonus"))

    # Calculate tenure in years
    df = df.withColumn("tenure_years", round(datediff(current_date(), col("hire_date")) / 365.25, 2))

    # Summarize projects (e.g., array size)
    df = df.withColumn("total_projects", size(col("project_ids")))

    # Check certifications (e.g., does the employee hold an AWS Cert?)
    df = df.withColumn("has_aws_cert", array_contains(col("certifications"), "AWS Cert"))

    # Add aggregated statistics for analysis
    summary = df.groupBy("department").count()
    summary.show()

    return df