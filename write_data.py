def write_data(df, output_path, format="delta"):
    """
    Write transformed data to an output location.

    Args:
        df (DataFrame): Data to save.
        output_path (str): Destination path for the data.
        format (str): Output format ('csv', 'json', 'delta', etc.).
    """
    if format in ["delta", "parquet"]:
        df.write.mode("overwrite").format(format).save(output_path)
    elif format == "csv":
        df.write.options(header=True).csv(output_path)
    else:
        raise ValueError("Unsupported write format provided.")