# Databricks Data Pipeline

A production-ready, end-to-end data pipeline built with Databricks, PySpark, and Delta Lake for scalable data engineering workflows.

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)

## 🎯 Overview

This repository provides a comprehensive data pipeline framework that demonstrates best practices for:
- **Data Ingestion**: Load raw data from multiple sources (CSV, JSON, Parquet)
- **Data Transformation**: Clean, enrich, and transform data with PySpark
- **Data Validation**: Ensure data quality with configurable validation rules
- **Data Output**: Write processed data to Delta Lake or Parquet format
- **Monitoring**: Built-in logging and metrics tracking

## 🏗️ Architecture

The pipeline follows a modular architecture with clear separation of concerns:

```
Data Sources → Ingestion → Transformation → Validation → Output
                  ↓            ↓              ↓           ↓
              [Bronze]     [Silver]       [Quality]   [Gold]
```

### Pipeline Stages:
1. **Bronze Layer**: Raw data ingestion with schema enforcement
2. **Silver Layer**: Data transformation and enrichment
3. **Gold Layer**: Analytics-ready data with quality validation

## ✨ Features

- 🚀 **Modular Design**: Reusable components for ingestion, transformation, and output
- 🔍 **Data Quality**: Configurable validation rules (nullability, uniqueness, range checks)
- ⚙️ **Configuration-Driven**: YAML-based configuration for sources, outputs, and rules
- 📊 **Schema Management**: Predefined schemas with support for complex types (structs, arrays, maps)
- 📝 **Comprehensive Logging**: Built-in logging with metrics tracking
- 🎯 **Spark Optimization**: Pre-configured Spark settings for optimal performance
- 🧪 **Example Scripts**: Ready-to-use examples for common scenarios

## 📁 Project Structure

```
databricks-data-pipeline/
├── src/
│   ├── pipeline/           # Core pipeline modules
│   │   ├── ingestion.py    # Data ingestion logic
│   │   ├── transformation.py # Data transformation logic
│   │   └── write_data.py   # Data output logic
│   └── utils/              # Utility modules
│       ├── config_reader.py    # Configuration management
│       ├── data_validator.py   # Data quality validation
│       ├── logger.py           # Custom logging
│       ├── spark_utils.py      # Spark session and schema utilities
│       └── utils.py            # General utilities
├── config/                 # Configuration files
│   ├── pipeline_config.yaml        # Pipeline settings
│   └── data_quality_rules.yaml     # Validation rules
├── data/                   # Sample data files
│   └── sample_data.csv
├── examples/               # Example usage scripts
│   ├── basic_usage.py
│   └── data_quality_example.py
├── tests/                  # Unit and integration tests
├── docs/                   # Additional documentation
├── run_pipeline.py         # Main pipeline orchestrator
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

**New to this project?** Check out the [Quick Start Guide](docs/QUICKSTART.md) for a step-by-step tutorial!

```bash
# Clone and setup
git clone https://github.com/wibnudixon/databricks-data-pipeline.git
cd databricks-data-pipeline
pip install -r requirements.txt

# Run the pipeline
python run_pipeline.py
```

## 🚀 Setup

### Prerequisites
- Python 3.8+
- Apache Spark 3.4+ (or Databricks Runtime)
- Java 11+ (for local Spark execution)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/wibnudixon/databricks-data-pipeline.git
cd databricks-data-pipeline
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the pipeline**
Edit `config/pipeline_config.yaml` to match your environment:
```yaml
paths:
  bronze: "dbfs:/mnt/bronze"  # Or local path: "data/bronze"
  silver: "dbfs:/mnt/silver"
  gold: "dbfs:/mnt/gold"
```

## 📖 Usage

### Quick Start

Run the complete pipeline with default settings:
```bash
python run_pipeline.py
```

### Custom Configuration

Run with custom input and output:
```bash
python run_pipeline.py \
  --input data/sample_data.csv \
  --output output/processed_data \
  --config config/pipeline_config.yaml
```

### Programmatic Usage

```python
from src.pipeline import ingest_data, transform_data, write_data

# Step 1: Ingest data
df = ingest_data("data/sample_data.csv", format="csv")

# Step 2: Transform data
df_transformed = transform_data(df)

# Step 3: Write data
write_data(df_transformed, "output/data", format="parquet")
```

### Using Individual Components

**Configuration Management:**
```python
from src.utils import ConfigReader

config = ConfigReader("config/pipeline_config.yaml")
bronze_path = config.get("paths.bronze")
```

**Data Quality Validation:**
```python
from src.utils import DataQualityValidator

validator = DataQualityValidator("config/data_quality_rules.yaml")
results = validator.run_validation(df, "employee_data")
report = validator.generate_quality_report(results)
```

**Spark Session Management:**
```python
from src.utils import SparkSessionManager

spark = SparkSessionManager.get_spark_session(
    app_name="MyPipeline",
    configs={"spark.sql.shuffle.partitions": "100"}
)
```

## ⚙️ Configuration

### Pipeline Configuration (`config/pipeline_config.yaml`)

Configure data sources, outputs, and Spark settings:
```yaml
sources:
  employee_data:
    path: "data/employee_data.csv"
    format: "csv"
    schema: "employee"

output:
  format: "delta"
  mode: "overwrite"
  partition_columns: ["department", "hire_year"]

spark:
  shuffle_partitions: 200
  adaptive_enabled: true
```

### Data Quality Rules (`config/data_quality_rules.yaml`)

Define validation rules for your datasets:
```yaml
rules:
  employee_data:
    - column: "id"
      checks:
        - type: "not_null"
        - type: "unique"
    - column: "salary"
      checks:
        - type: "range"
          min: 30000
          max: 500000
```

## 📚 Examples

### Basic Pipeline
See `examples/basic_usage.py` for a complete example:
```bash
python examples/basic_usage.py
```

### Data Quality Validation
See `examples/data_quality_example.py`:
```bash
python examples/data_quality_example.py
```

## 🧪 Testing

Run tests (once implemented):
```bash
pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.
