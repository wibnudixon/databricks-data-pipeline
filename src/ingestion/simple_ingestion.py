"""
Simple data ingestion without schema enforcement.
Adapted from complex-schema-enhancements and copilot/update-readme-and-upload-files branches.
"""
from pyspark.sql import SparkSession


def ingest_data_simple(file_path, format="csv", options=None):
    """
    Ingest raw data files into a Spark DataFrame with flexible options.

    Args:
        file_path (str): Path to the input data file.
        format (str): Data format ('csv', 'json', 'parquet', etc.).
        options (dict): Additional options like delimiter, header, etc.

    Returns:
        DataFrame: Spark DataFrame containing the ingested data.
    """
    if options is None:
        options = {}
    
    spark = SparkSession.builder.appName("DataIngestion").getOrCreate()

    if format == "csv":
        options.setdefault("header", "true")
        df = spark.read.options(**options).csv(file_path)
    elif format == "json":
        df = spark.read.options(**options).json(file_path)
    elif format == "parquet":
        df = spark.read.parquet(file_path)
    else:
        raise ValueError(f"Unsupported format: {format}")

    return df
