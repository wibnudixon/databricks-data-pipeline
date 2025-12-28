# Quick Start Guide

Get started with the Databricks Data Pipeline in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Git

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/wibnudixon/databricks-data-pipeline.git
cd databricks-data-pipeline

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Verify Installation

```bash
# Check if PySpark is installed
python -c "import pyspark; print(f'PySpark version: {pyspark.__version__}')"
```

## Step 3: Run Your First Pipeline

### Option A: Using the Interactive Examples

```bash
# Run the interactive examples script
python examples.py
```

Then select an option from the menu (1-5).

### Option B: Run a Simple Pipeline

Create a file `my_first_pipeline.py`:

```python
from src.pipeline import DataPipeline

# Initialize pipeline
pipeline = DataPipeline()

# Run simple pipeline
df = pipeline.run_simple_pipeline(
    input_path="data/input/sample_data.csv",
    output_path="data/output/my_first_output",
    format="csv"
)

print(f"Success! Processed {df.count()} records")
```

Run it:
```bash
python my_first_pipeline.py
```

## Step 4: Explore the Results

```bash
# Check the output directory
ls -la data/output/
```

## Step 5: Try More Features

### Use Schema Enforcement

```python
from src.ingestion import ingest_data_with_schema, get_complex_employee_schema

schema = get_complex_employee_schema()
df = ingest_data_with_schema("data/input/sample_data.csv", schema)
```

### Add Data Validation

```python
from src.validation import DataQualityValidator

validator = DataQualityValidator("config/data_quality_rules.yaml")
results = validator.run_validation(df, "employee_data")
report = validator.generate_quality_report(results)
print(f"Quality Score: {report['success_rate']:.2f}%")
```

### Use Delta Lake

```python
from src.pipeline import DataPipeline

pipeline = DataPipeline()
pipeline.run_delta_pipeline(
    input_path="data/input/sample_data.csv",
    table_name="data/output/gold/employees",
    partition_by=["department"]
)
```

## Common Issues

### Import Errors

If you get import errors, make sure you're running from the project root:

```bash
cd /path/to/databricks-data-pipeline
export PYTHONPATH=$PWD:$PYTHONPATH
python my_script.py
```

### Spark Not Found

Install PySpark:
```bash
pip install pyspark
```

### Configuration File Not Found

Make sure configuration files exist:
```bash
ls config/
# Should show: data_quality_rules.yaml  pipeline_config.yaml
```

## Next Steps

1. **Read the README**: Learn about the architecture and features
   ```bash
   cat README.md
   ```

2. **Explore the docs**: Detailed documentation
   ```bash
   cat docs/ARCHITECTURE.md
   cat docs/MIGRATION.md
   ```

3. **Customize configuration**: Edit `config/pipeline_config.yaml`

4. **Add your data**: Place your CSV/JSON/Parquet files in `data/input/`

5. **Build your pipeline**: Use the examples as templates

## Quick Reference

### Directory Structure
```
databricks-data-pipeline/
├── src/              # Source code
├── config/           # Configuration files
├── data/             # Data directories
│   ├── input/        # Place your input data here
│   └── output/       # Output will be written here
├── docs/             # Documentation
├── examples.py       # Interactive examples
└── requirements.txt  # Dependencies
```

### Key Files
- `src/pipeline.py` - Main pipeline orchestrator
- `config/pipeline_config.yaml` - Pipeline configuration
- `examples.py` - Example scripts
- `README.md` - Full documentation

### Main Components
- **Ingestion**: `src/ingestion/`
- **Transformation**: `src/transformation/`
- **Validation**: `src/validation/`
- **Writers**: `src/writers/`
- **Utils**: `src/utils/`

## Getting Help

- Check `README.md` for comprehensive documentation
- Review `examples.py` for usage patterns
- Read `docs/ARCHITECTURE.md` for detailed component info
- See `docs/MIGRATION.md` if migrating from old structure

## Congratulations! 🎉

You've successfully set up the Databricks Data Pipeline!

Now you can:
- Process data from multiple sources
- Apply transformations and validations
- Write to various formats (Parquet, Delta Lake, CSV)
- Build production-ready data pipelines
