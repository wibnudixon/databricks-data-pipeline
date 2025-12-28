"""
Example: Data Quality Validation

This example demonstrates how to use the data quality validator
to check data against predefined rules.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import ingest_data
from src.utils import DataQualityValidator, PipelineLogger

def main():
    """Run data quality validation example."""
    
    # Initialize logger
    logger = PipelineLogger("ValidationExample").get_logger()
    logger.info("Starting data quality validation example")
    
    # Ingest data
    logger.info("Ingesting data...")
    input_file = "data/sample_data.csv"
    df = ingest_data(input_file, format="csv")
    
    # Initialize validator
    validator = DataQualityValidator("config/data_quality_rules.yaml")
    
    # Run validation
    logger.info("Running data quality checks...")
    results = validator.run_validation(df, "employee_data")
    
    # Generate report
    report = validator.generate_quality_report(results)
    
    # Display results
    logger.info("=" * 60)
    logger.info("DATA QUALITY REPORT")
    logger.info("=" * 60)
    logger.info(f"Total Checks: {report['total_checks']}")
    logger.info(f"Passed: {report['passed_checks']}")
    logger.info(f"Failed: {report['failed_checks']}")
    logger.info(f"Success Rate: {report['success_rate']:.2f}%")
    logger.info("=" * 60)
    
    # Show details of failed checks
    failed_checks = [r for r in results if not r['passed']]
    if failed_checks:
        logger.warning("Failed checks:")
        for check in failed_checks:
            logger.warning(f"  - {check['check']} on column '{check['column']}'")
    else:
        logger.info("All data quality checks passed!")

if __name__ == "__main__":
    main()
