from pyspark.sql import SparkSession
from pyspark.sql.types import *

def ingest_data(file_path, format="csv"):
    """
    Ingest raw data and enforce schema with complex structures.

    Args:
        file_path (str): Path to the input data file.
        format (str): File format ('csv', 'json', 'parquet').

    Returns:
        DataFrame: Spark DataFrame containing raw data.
    """
    spark = SparkSession.builder.appName("DataIngestion").getOrCreate()

    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("employee_name", StringType(), True),
        StructField("department", StringType(), True),
        StructField("role", StringType(), True),
        StructField("hire_date", DateType(), True),
        StructField("salary", DecimalType(10, 2), True),
        StructField("bonus", DecimalType(10, 2), True),
        StructField("address", StructType([
            StructField("street", StringType(), True),
            StructField("city", StringType(), True),
            StructField("state", StringType(), True),
            StructField("zip", StringType(), True)
        ]), True),
        StructField("performance", StructType([
            StructField("score", IntegerType(), True),
            StructField("last_review_date", DateType(), True)
        ]), True),
        StructField("satisfaction_level", DoubleType(), True),
        StructField("projects_count", IntegerType(), True),
        StructField("project_ids", ArrayType(IntegerType()), True),
        StructField("certifications", ArrayType(StringType()), True),
        StructField("employment_type", StringType(), True),
        StructField("region", StringType(), True),
        StructField("additional_info", MapType(StringType(), StringType()), True),
        StructField("age", IntegerType(), True),
        StructField("gender", StringType(), True),
        StructField("marital_status", StringType(), True),
        StructField("promotions_count", IntegerType(), True),
        StructField("education_level", StringType(), True),
        StructField("hire_timestamp", TimestampType(), True),
        StructField("dependents", IntegerType(), True)
    ])

    return spark.read.format(format).schema(schema).option("header", True).load(file_path)