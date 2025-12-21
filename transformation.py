from pyspark.sql.functions import col, when


def transform_data(df):
    """
    Apply data transformations to clean and process raw data.

    Args:
        df (DataFrame): Spark DataFrame containing raw data.

    Returns:
        DataFrame: Transformed Spark DataFrame.
    """
    # Drop duplicates
    df = df.dropDuplicates()

    # Fill missing values
    df = df.fillna({"column_name": "default_value"})

    # Add a calculated column
    df = df.withColumn(
        "status",
        when(col("value") > 100, "High").otherwise("Low")
    )

    return df