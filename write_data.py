def write_data(df, output_path, format="parquet", partition_by=None):
    """
    Write transformed data to an output location.

    Args:
        df (DataFrame): Transformed Spark DataFrame.
        output_path (str): Destination for the output data.
        format (str): Output file format ('csv', 'json', 'parquet').
        partition_by (list): Columns to partition the data by.
    """
    writer = df.write.mode("overwrite").format(format)
    if partition_by:
        writer = writer.partitionBy(*partition_by)
    writer.save(output_path)