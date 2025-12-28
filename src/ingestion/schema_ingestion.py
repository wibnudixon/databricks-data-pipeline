"""
Schema-enforced data ingestion with complex data types.
Adapted from main and copilot/manage-repository-branches branches.
"""
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, 
    DoubleType, DateType, DecimalType, TimestampType,
    ArrayType, MapType
)


def get_complex_employee_schema():
    """
    Define complex schema for employee data with nested structures.
    
    Returns:
        StructType: Schema definition for employee data.
    """
    return StructType([
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


def ingest_data_with_schema(file_path, schema, format="csv", options=None):
    """
    Ingest raw data with enforced schema and complex structures.

    Args:
        file_path (str): Path to the input data file.
        schema (StructType): Schema to enforce on the data.
        format (str): File format ('csv', 'json', 'parquet').
        options (dict): Additional read options.

    Returns:
        DataFrame: Spark DataFrame containing raw data with enforced schema.
    """
    if options is None:
        options = {"header": "true"}
    
    spark = SparkSession.builder.appName("DataIngestion").getOrCreate()
    
    return spark.read.format(format).schema(schema).options(**options).load(file_path)
