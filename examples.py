"""
Example usage of the unified Databricks data pipeline.
This script demonstrates how to use the new modular architecture.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def example_simple_pipeline():
    """
    Example 1: Simple pipeline without schema enforcement.
    """
    print("=" * 60)
    print("Example 1: Simple Pipeline")
    print("=" * 60)
    
    from src.pipeline import DataPipeline
    
    # Initialize pipeline
    pipeline = DataPipeline()
    
    # Run simple pipeline
    try:
        df = pipeline.run_simple_pipeline(
            input_path="data/input/sample_data.csv",
            output_path="data/output/bronze/simple",
            format="csv"
        )
        print(f"✓ Simple pipeline completed successfully!")
        print(f"  Records processed: {df.count()}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def example_complex_pipeline():
    """
    Example 2: Complex pipeline with schema enforcement and transformations.
    """
    print("=" * 60)
    print("Example 2: Complex Pipeline with Schema Enforcement")
    print("=" * 60)
    
    from src.pipeline import DataPipeline
    
    # Initialize pipeline
    pipeline = DataPipeline()
    
    # Run complex pipeline
    try:
        df = pipeline.run_complex_pipeline(
            input_path="data/input/sample_data.csv",
            output_path="data/output/silver/complex",
            format="csv",
            validate=False  # Set to True if validation rules are configured
        )
        print(f"✓ Complex pipeline completed successfully!")
        print(f"  Records processed: {df.count()}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def example_individual_modules():
    """
    Example 3: Using individual modules directly.
    """
    print("=" * 60)
    print("Example 3: Using Individual Modules")
    print("=" * 60)
    
    from src.ingestion import ingest_data_simple
    from src.writers import write_data
    
    try:
        # Ingest data
        print("  1. Ingesting data...")
        df = ingest_data_simple("data/input/sample_data.csv", format="csv")
        print(f"     ✓ Ingested {df.count()} records")
        
        # Show first few rows
        print("  2. Sample data:")
        df.show(5)
        
        # Write data
        print("  3. Writing data...")
        write_data(df, "data/output/bronze/modular", format="parquet")
        print(f"     ✓ Data written successfully")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def example_with_validation():
    """
    Example 4: Using data validation.
    """
    print("=" * 60)
    print("Example 4: Data Validation")
    print("=" * 60)
    
    from src.ingestion import ingest_data_simple
    from src.validation import DataQualityValidator
    
    try:
        # Ingest data
        print("  1. Ingesting data...")
        df = ingest_data_simple("data/input/sample_data.csv", format="csv")
        print(f"     ✓ Ingested {df.count()} records")
        
        # Validate data (requires data_quality_rules.yaml to be configured)
        print("  2. Validating data quality...")
        try:
            validator = DataQualityValidator("config/data_quality_rules.yaml")
            results = validator.run_validation(df, "employee_data")
            report = validator.generate_quality_report(results)
            
            print(f"     ✓ Validation completed")
            print(f"       - Total checks: {report['total_checks']}")
            print(f"       - Passed: {report['passed_checks']}")
            print(f"       - Failed: {report['failed_checks']}")
            print(f"       - Success rate: {report['success_rate']:.2f}%")
        except FileNotFoundError:
            print("     ⚠ Validation rules file not found, skipping validation")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def print_menu():
    """Print example menu."""
    print("\n" + "=" * 60)
    print("Databricks Data Pipeline - Example Usage")
    print("=" * 60)
    print("\nAvailable examples:")
    print("  1. Simple pipeline")
    print("  2. Complex pipeline with schema enforcement")
    print("  3. Using individual modules")
    print("  4. Data validation")
    print("  5. Run all examples")
    print("  0. Exit")
    print()


def main():
    """Main function to run examples."""
    
    while True:
        print_menu()
        choice = input("Select an example (0-5): ").strip()
        
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            example_simple_pipeline()
        elif choice == "2":
            example_complex_pipeline()
        elif choice == "3":
            example_individual_modules()
        elif choice == "4":
            example_with_validation()
        elif choice == "5":
            example_simple_pipeline()
            example_complex_pipeline()
            example_individual_modules()
            example_with_validation()
        else:
            print("Invalid choice. Please select 0-5.")
        
        if choice != "0":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    print("\n" + "🚀 " * 20)
    print("DATABRICKS DATA PIPELINE - UNIFIED ARCHITECTURE")
    print("🚀 " * 20 + "\n")
    print("This script demonstrates the new modular architecture.")
    print("Make sure you have:")
    print("  1. Installed dependencies: pip install -r requirements.txt")
    print("  2. Sample data in: data/input/sample_data.csv")
    print("  3. Configuration files in: config/")
    
    proceed = input("\nReady to proceed? (y/n): ").strip().lower()
    
    if proceed == 'y':
        main()
    else:
        print("Exiting...")
