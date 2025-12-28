# Quick Start Guide

This guide will help you get started with the Databricks Data Pipeline quickly.

## Prerequisites

- Python 3.8 or higher
- Java 11+ (for local Spark execution)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/wibnudixon/databricks-data-pipeline.git
cd databricks-data-pipeline
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Run the structure verification script:

```bash
python verify_structure.py
```

You should see all green checkmarks (✓).

## Running Your First Pipeline

### Option 1: Use the Main Pipeline Runner

The simplest way to run the pipeline with default settings:

```bash
python run_pipeline.py
```

This will:
1. Read from `data/sample_data.csv`
2. Apply transformations
3. Write output to `output/data` (in Parquet format)

### Option 2: Run with Custom Parameters

Specify custom input and output paths:

```bash
python run_pipeline.py \
  --input data/my_custom_data.csv \
  --output output/my_output \
  --config config/pipeline_config.yaml
```

### Option 3: Run Example Scripts

Try the basic usage example:

```bash
python examples/basic_usage.py
```

Or the data quality validation example:

```bash
python examples/data_quality_example.py
```

### Option 4: Use as a Library

Create your own script:

```python
from src.pipeline import ingest_data, transform_data, write_data

# Ingest
df = ingest_data("data/sample_data.csv", format="csv")

# Transform
df_transformed = transform_data(df)

# Write
write_data(df_transformed, "output/results", format="parquet")
```

## Configuration

### Pipeline Configuration

Edit `config/pipeline_config.yaml` to customize:

```yaml
paths:
  bronze: "data/bronze"      # Raw data location
  silver: "data/silver"      # Transformed data location
  gold: "data/gold"          # Final analytics-ready data

sources:
  my_data:
    path: "data/my_file.csv"
    format: "csv"
    
output:
  format: "parquet"          # or "delta", "csv"
  mode: "overwrite"          # or "append"
```

### Data Quality Rules

Edit `config/data_quality_rules.yaml` to define validation rules:

```yaml
rules:
  my_dataset:
    - column: "id"
      checks:
        - type: "not_null"
        - type: "unique"
    - column: "amount"
      checks:
        - type: "range"
          min: 0
          max: 1000000
```

## Project Structure

```
databricks-data-pipeline/
├── src/
│   ├── pipeline/          # Core pipeline logic
│   └── utils/             # Utilities (config, logging, validation)
├── config/                # Configuration files
├── data/                  # Data files
├── examples/              # Example scripts
├── tests/                 # Tests
├── docs/                  # Documentation
└── run_pipeline.py        # Main entry point
```

## Common Tasks

### Add a New Data Source

1. Add source configuration to `config/pipeline_config.yaml`
2. Ensure data format is supported (csv, json, parquet)
3. Run the pipeline with your new source

### Add Custom Transformations

Edit `src/pipeline/transformation.py` and add your logic to the `transform_data` function:

```python
def transform_data(df):
    # Existing transformations...
    
    # Your custom transformation
    df = df.withColumn("custom_field", col("field1") + col("field2"))
    
    return df
```

### Add Validation Rules

Add rules to `config/data_quality_rules.yaml`:

```yaml
rules:
  your_dataset:
    - column: "email"
      checks:
        - type: "format"
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

### Change Output Format

Modify the output format in your script or configuration:

```python
write_data(df, "output/path", format="delta")  # Use Delta Lake format
```

## Troubleshooting

### PySpark Not Found

Ensure you've installed requirements:
```bash
pip install -r requirements.txt
```

### Java Not Found

Install Java 11 or higher and ensure it's in your PATH.

### Import Errors

Make sure you're running from the project root directory and the virtual environment is activated.

### Permission Errors

On Unix-like systems, you may need to make the script executable:
```bash
chmod +x run_pipeline.py
```

## Next Steps

- Read the [Architecture Documentation](docs/ARCHITECTURE.md) to understand the design
- Check out the [README](README.md) for comprehensive documentation
- Look at example scripts in the `examples/` directory
- Write tests for your custom code in the `tests/` directory

## Getting Help

- Check the documentation in the `docs/` folder
- Open an issue on GitHub for bugs or questions
- Review example scripts for common use cases

## Useful Commands

```bash
# Verify structure
python verify_structure.py

# Run main pipeline
python run_pipeline.py

# Run with custom config
python run_pipeline.py --config config/my_config.yaml

# Run tests (once implemented)
pytest tests/

# Check Python syntax
python -m py_compile src/**/*.py
```

Happy data engineering! 🚀
