"""
Main Pipeline Runner
Orchestrates the complete data pipeline from ingestion to output.
"""
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logger import PipelineLogger
from src.utils.config_reader import ConfigReader
from src.utils.spark_utils import SparkSessionManager
from src.pipeline.ingestion import ingest_data
from src.pipeline.transformation import transform_data
from src.pipeline.write_data import write_data


def run_pipeline(config_path="config/pipeline_config.yaml", input_file=None, output_path=None):
    """
    Execute the complete data pipeline.
    
    Args:
        config_path (str): Path to pipeline configuration file
        input_file (str): Optional input file path (overrides config)
        output_path (str): Optional output path (overrides config)
    """
    # Initialize logger
    logger = PipelineLogger("DataPipeline").get_logger()
    logger.info("Starting Databricks Data Pipeline")
    
    try:
        # Load configuration
        config = ConfigReader(config_path)
        logger.info(f"Configuration loaded from {config_path}")
        
        # Initialize Spark session
        spark_configs = {
            "spark.sql.adaptive.enabled": str(config.get("spark.adaptive_enabled", True)).lower(),
            "spark.sql.shuffle.partitions": str(config.get("spark.shuffle_partitions", 200)),
            "spark.databricks.delta.optimizeWrite.enabled": str(config.get("spark.optimize_write", True)).lower(),
            "spark.databricks.delta.autoCompact.enabled": str(config.get("spark.auto_compact", True)).lower()
        }
        
        spark = SparkSessionManager.get_spark_session(
            app_name=config.get("spark.app_name", "DataPipeline"),
            configs=spark_configs
        )
        logger.info("Spark session initialized")
        
        # Step 1: Data Ingestion
        logger.info("=" * 60)
        logger.info("STEP 1: Data Ingestion")
        logger.info("=" * 60)
        
        # Determine input file
        if input_file:
            file_path = input_file
            file_format = Path(input_file).suffix[1:]  # Extract format from extension
        else:
            # Use first source from config as default
            sources = config.get("sources", {})
            if sources:
                first_source = list(sources.values())[0]
                file_path = first_source.get("path", "data/sample_data.csv")
                file_format = first_source.get("format", "csv")
            else:
                file_path = "data/sample_data.csv"
                file_format = "csv"
        
        logger.info(f"Ingesting data from: {file_path}")
        df = ingest_data(file_path, format=file_format)
        record_count = df.count()
        logger.info(f"Successfully ingested {record_count} records")
        
        # Step 2: Data Transformation
        logger.info("=" * 60)
        logger.info("STEP 2: Data Transformation")
        logger.info("=" * 60)
        
        df_transformed = transform_data(df)
        logger.info(f"Data transformation completed")
        
        # Step 3: Write Data
        logger.info("=" * 60)
        logger.info("STEP 3: Writing Data")
        logger.info("=" * 60)
        
        # Determine output path
        if output_path:
            final_output_path = output_path
        else:
            final_output_path = config.get("paths.gold", "output/data")
        
        output_format = config.get("output.format", "parquet")
        partition_cols = config.get("output.partition_columns", None)
        
        logger.info(f"Writing data to: {final_output_path}")
        logger.info(f"Output format: {output_format}")
        if partition_cols:
            logger.info(f"Partitioning by: {partition_cols}")
        
        write_data(df_transformed, final_output_path, format=output_format, partition_by=partition_cols)
        logger.info("Data successfully written")
        
        # Pipeline complete
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}", exc_info=True)
        raise
    finally:
        # Stop Spark session
        if 'spark' in locals():
            spark.stop()
            logger.info("Spark session stopped")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Databricks Data Pipeline")
    parser.add_argument(
        "--config",
        default="config/pipeline_config.yaml",
        help="Path to pipeline configuration file"
    )
    parser.add_argument(
        "--input",
        help="Input file path (overrides config)"
    )
    parser.add_argument(
        "--output",
        help="Output path (overrides config)"
    )
    
    args = parser.parse_args()
    
    run_pipeline(
        config_path=args.config,
        input_file=args.input,
        output_path=args.output
    )
