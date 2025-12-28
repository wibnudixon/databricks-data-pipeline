"""
Main pipeline orchestrator for the Databricks data pipeline.
Combines components from all branches into a unified workflow.
"""
from src.ingestion import ingest_data_simple, ingest_data_with_schema, get_complex_employee_schema
from src.transformation import transform_data, flatten_nested_fields
from src.validation import DataQualityValidator
from src.writers import write_data, write_delta_table
from src.utils import PipelineLogger, ConfigReader, SparkSessionManager


class DataPipeline:
    """
    Unified data pipeline orchestrator.
    """
    
    def __init__(self, config_path="config/pipeline_config.yaml"):
        """
        Initialize pipeline with configuration.
        
        Args:
            config_path (str): Path to pipeline configuration file.
        """
        self.logger = PipelineLogger("DataPipeline").get_logger()
        try:
            self.config = ConfigReader(config_path)
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}. Using defaults.")
            self.config = None
        
        self.spark = SparkSessionManager.get_spark_session()
        self.validator = None
    
    def run_simple_pipeline(self, input_path, output_path, format="csv"):
        """
        Run simple pipeline without schema enforcement.
        
        Args:
            input_path (str): Input data path.
            output_path (str): Output data path.
            format (str): Data format.
        """
        self.logger.info(f"Starting simple pipeline: {input_path} -> {output_path}")
        
        # Ingest
        df = ingest_data_simple(input_path, format=format)
        self.logger.info(f"Ingested {df.count()} records")
        
        # Write
        write_data(df, output_path, format=format)
        self.logger.info(f"Pipeline completed successfully")
        
        return df
    
    def run_complex_pipeline(self, input_path, output_path, format="csv", validate=False):
        """
        Run complex pipeline with schema enforcement and transformations.
        
        Args:
            input_path (str): Input data path.
            output_path (str): Output data path.
            format (str): Data format.
            validate (bool): Enable data quality validation.
        """
        self.logger.info(f"Starting complex pipeline: {input_path} -> {output_path}")
        
        # Ingest with schema
        schema = get_complex_employee_schema()
        df = ingest_data_with_schema(input_path, schema, format=format)
        self.logger.info(f"Ingested {df.count()} records with schema enforcement")
        
        # Validate (optional)
        if validate and self.validator:
            results = self.validator.run_validation(df, "employee_data")
            report = self.validator.generate_quality_report(results)
            self.logger.info(f"Validation: {report['passed_checks']}/{report['total_checks']} checks passed")
        
        # Transform
        df_transformed = transform_data(df)
        self.logger.info(f"Transformation completed")
        
        # Write
        write_data(df_transformed, output_path, format=format)
        self.logger.info(f"Pipeline completed successfully")
        
        return df_transformed
    
    def run_delta_pipeline(self, input_path, table_name, format="csv", partition_by=None):
        """
        Run pipeline with Delta Lake output.
        
        Args:
            input_path (str): Input data path.
            table_name (str): Delta table name.
            format (str): Input data format.
            partition_by (list): Columns to partition by.
        """
        self.logger.info(f"Starting Delta pipeline: {input_path} -> {table_name}")
        
        # Ingest
        df = ingest_data_simple(input_path, format=format)
        self.logger.info(f"Ingested {df.count()} records")
        
        # Write as Delta
        write_delta_table(df, table_name, partition_by=partition_by)
        self.logger.info(f"Delta table created: {table_name}")
        
        return df


if __name__ == "__main__":
    # Example usage
    pipeline = DataPipeline()
    
    # Simple pipeline example
    # pipeline.run_simple_pipeline(
    #     input_path="data/input/sample_data.csv",
    #     output_path="data/output/processed_data",
    #     format="csv"
    # )
