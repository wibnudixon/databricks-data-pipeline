"""
Advanced transformation functions for complex data structures.
"""
from pyspark.sql.functions import col, struct, explode, array, create_map, lit


def flatten_nested_fields(df, nested_field, prefix=None):
    """
    Flatten a nested struct field into individual columns.
    
    Args:
        df (DataFrame): Input DataFrame.
        nested_field (str): Name of the nested field to flatten.
        prefix (str): Optional prefix for flattened column names.
    
    Returns:
        DataFrame: DataFrame with flattened fields.
    """
    if prefix is None:
        prefix = nested_field
    
    nested_cols = df.select(f"{nested_field}.*").columns
    
    for nested_col in nested_cols:
        df = df.withColumn(f"{prefix}_{nested_col}", col(f"{nested_field}.{nested_col}"))
    
    return df.drop(nested_field)


def calculate_derived_metrics(df, base_column, operations):
    """
    Calculate derived metrics based on specified operations.
    
    Args:
        df (DataFrame): Input DataFrame.
        base_column (str): Column to base calculations on.
        operations (dict): Dictionary of {new_column_name: operation_function}.
    
    Returns:
        DataFrame: DataFrame with additional derived columns.
    """
    for new_col, operation in operations.items():
        df = df.withColumn(new_col, operation(col(base_column)))
    
    return df


def explode_array_column(df, array_column, new_column_name=None):
    """
    Explode an array column into separate rows.
    
    Args:
        df (DataFrame): Input DataFrame.
        array_column (str): Name of array column to explode.
        new_column_name (str): Name for exploded column (defaults to array_column).
    
    Returns:
        DataFrame: DataFrame with exploded array.
    """
    if new_column_name is None:
        new_column_name = f"{array_column}_item"
    
    return df.withColumn(new_column_name, explode(col(array_column)))
