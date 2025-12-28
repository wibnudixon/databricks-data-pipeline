"""
Example: Basic Pipeline Usage

This example demonstrates the basic usage of the data pipeline
with a simple CSV file.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import ingest_data, transform_data, write_data
from src.utils import PipelineLogger

def main():
    """Run a basic example of the pipeline."""
    
    # Initialize logger
    logger = PipelineLogger("BasicExample").get_logger()
    logger.info("Starting basic pipeline example")
    
    # Step 1: Ingest data
    logger.info("Step 1: Ingesting data...")
    input_file = "data/sample_data.csv"
    df = ingest_data(input_file, format="csv")
    
    logger.info(f"Ingested {df.count()} records")
    logger.info("Sample data:")
    df.show(5)
    
    # Step 2: Transform data
    logger.info("Step 2: Transforming data...")
    df_transformed = transform_data(df)
    
    logger.info("Transformed data sample:")
    df_transformed.show(5)
    
    # Step 3: Write data
    logger.info("Step 3: Writing data...")
    output_path = "output/example_output"
    write_data(df_transformed, output_path, format="parquet")
    
    logger.info(f"Data written to: {output_path}")
    logger.info("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
