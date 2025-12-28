"""
Data writing utilities for the pipeline.
Adapted from write_data.py in main branch with enhancements.
"""


def write_data(df, output_path, format="parquet", partition_by=None, mode="overwrite"):
    """
    Write transformed data to an output location.

    Args:
        df (DataFrame): Transformed Spark DataFrame.
        output_path (str): Destination for the output data.
        format (str): Output file format ('csv', 'json', 'parquet', 'delta').
        partition_by (list): Columns to partition the data by.
        mode (str): Write mode ('overwrite', 'append', 'ignore', 'error').
    """
    writer = df.write.mode(mode).format(format)
    
    if partition_by:
        writer = writer.partitionBy(*partition_by)
    
    writer.save(output_path)


def write_delta_table(df, table_name, mode="overwrite", partition_by=None, 
                      optimize_write=True, auto_compact=True):
    """
    Write data as Delta table with optimizations.
    
    Args:
        df (DataFrame): DataFrame to write.
        table_name (str): Delta table name/path.
        mode (str): Write mode ('overwrite', 'append', 'merge').
        partition_by (list): Columns to partition by.
        optimize_write (bool): Enable optimized writes.
        auto_compact (bool): Enable auto-compaction.
    """
    writer = df.write.format("delta").mode(mode)
    
    if partition_by:
        writer = writer.partitionBy(*partition_by)
    
    if optimize_write:
        writer = writer.option("optimizeWrite", "true")
    
    if auto_compact:
        writer = writer.option("autoCompact", "true")
    
    writer.save(table_name)
