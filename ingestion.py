from pyspark.sql import SparkSession


def ingest_data(file_path, format="csv", options={}):
    """
    Ingest raw data files into a Spark DataFrame.

    Args:
        file_path (str): Path to the input data file.
        format (str): Data format ('csv', 'json', 'parquet', etc.).
        options (dict): Additional options like delimiter, header, etc.

    Returns:
        DataFrame: Spark DataFrame containing the ingested data.
    """
    spark = SparkSession.builder.appName("DataIngestion").getOrCreate()

    if format == "csv":
        options.setdefault("header", "true")  # Default: CSV with headers.
        df = spark.read.options(**options).csv(file_path)
    elif format == "json":
        df = spark.read.options(**options).json(file_path)
    elif format == "parquet":
        df = spark.read.parquet(file_path)
    else:
        raise ValueError("Unsupported format provided.")

    return df