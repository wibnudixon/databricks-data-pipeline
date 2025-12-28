from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

class SparkSessionManager:
    """Manage Spark session with optimized configurations."""
    
    @staticmethod
    def get_spark_session(app_name="DataPipeline", configs=None):
        """Create or get existing Spark session with optimizations."""
        builder = SparkSession.builder. appName(app_name)
        
        # Default optimized configurations
        default_configs = {
            "spark.sql.adaptive.enabled": "true",
            "spark.sql. adaptive.coalescePartitions. enabled": "true",
            "spark.sql.shuffle.partitions":  "200",
            "spark. databricks.delta.optimizeWrite.enabled": "true",
            "spark.databricks. delta.autoCompact.enabled": "true"
        }
        
        # Merge with custom configs
        if configs:
            default_configs. update(configs)
        
        for key, value in default_configs. items():
            builder = builder. config(key, value)
        
        return builder.getOrCreate()

def get_employee_schema():
    """Define schema for employee data."""
    return StructType([
        StructField("employee_id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("email", StringType(), False),
        StructField("department", StringType(), True),
        StructField("job_title", StringType(), True),
        StructField("salary", DoubleType(), True),
        StructField("hire_date", DateType(), True),
        StructField("manager_id", StringType(), True),
        StructField("location", StringType(), True)
    ])

def get_attendance_schema():
    """Define schema for attendance data."""
    return StructType([
        StructField("attendance_id", StringType(), False),
        StructField("employee_id", StringType(), False),
        StructField("date", DateType(), False),
        StructField("check_in_time", StringType(), True),
        StructField("check_out_time", StringType(), True),
        StructField("hours_worked", DoubleType(), True),
        StructField("status", StringType(), True)
    ])