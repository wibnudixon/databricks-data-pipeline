# Databricks Data Pipeline - Unified Architecture

## About
This repository demonstrates a comprehensive, production-ready data pipeline using Databricks, PySpark, and Delta Lake. The architecture consolidates best practices and features from multiple development branches into a unified, scalable solution for enterprise data engineering.

---

## Architecture Overview

### Unified Design Philosophy
This pipeline architecture integrates components from all development branches:
- **Main Branch**: Complex schema enforcement and nested data structures
- **Complex-Schema-Enhancements**: Flexible, schema-less ingestion
- **Copilot Branches**: Enhanced utilities, validation, and configuration management

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                             │
│         (CSV, JSON, Parquet, Delta, APIs, Databases)        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  INGESTION LAYER                            │
│  ┌──────────────────┐      ┌──────────────────────────┐   │
│  │ Simple Ingestion │      │ Schema-Enforced Ingestion│   │
│  │  (Flexible)      │      │  (Type-Safe)             │   │
│  └──────────────────┘      └──────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  VALIDATION LAYER                           │
│        ┌────────────────────────────────────┐              │
│        │  Data Quality Validator            │              │
│        │  - Null checks                     │              │
│        │  - Uniqueness validation           │              │
│        │  - Range validation                │              │
│        │  - Format validation (regex)       │              │
│        │  - Allowed values validation       │              │
│        └────────────────────────────────────┘              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               TRANSFORMATION LAYER                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Basic Transformations                               │  │
│  │  - Flatten nested structures                         │  │
│  │  - Calculate derived metrics                         │  │
│  │  - Aggregate statistics                              │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Advanced Transformations                            │  │
│  │  - Complex field extraction                          │  │
│  │  - Array/Map operations                              │  │
│  │  - Custom business logic                             │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  WRITING LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Parquet    │  │   Delta      │  │    CSV/JSON  │     │
│  │   (Bronze)   │  │ (Silver/Gold)│  │   (Export)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
databricks-data-pipeline/
├── src/                           # Source code modules
│   ├── __init__.py
│   ├── pipeline.py               # Main pipeline orchestrator
│   ├── ingestion/                # Data ingestion
│   │   ├── __init__.py
│   │   ├── simple_ingestion.py  # Flexible ingestion
│   │   └── schema_ingestion.py  # Schema-enforced ingestion
│   ├── transformation/           # Data transformations
│   │   ├── __init__.py
│   │   ├── basic_transformations.py
│   │   └── advanced_transformations.py
│   ├── validation/               # Data quality checks
│   │   ├── __init__.py
│   │   └── data_quality_validator.py
│   ├── writers/                  # Data writers
│   │   ├── __init__.py
│   │   └── data_writer.py
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── config_reader.py     # YAML config management
│       ├── logger.py            # Pipeline logging
│       └── spark_manager.py     # Spark session management
├── config/                       # Configuration files
│   ├── pipeline_config.yaml     # Pipeline settings
│   └── data_quality_rules.yaml  # Validation rules
├── data/                         # Data directories
│   ├── input/                   # Input data
│   └── output/                  # Output data (bronze/silver/gold)
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## Key Features

### 1. **Dual Ingestion Modes**
- **Simple Ingestion**: Flexible data loading without strict schema enforcement
- **Schema-Enforced Ingestion**: Type-safe loading with complex data structures (nested objects, arrays, maps)

### 2. **Comprehensive Data Validation**
- Configurable quality rules via YAML
- Multiple validation types: null checks, uniqueness, ranges, formats, allowed values
- Detailed quality reports with pass/fail metrics

### 3. **Advanced Transformations**
- Flatten nested structures (address, performance objects)
- Calculate derived metrics (tenure, compensation, project counts)
- Array and map operations (certifications, additional info)

### 4. **Multiple Output Formats**
- Parquet (columnar, efficient)
- Delta Lake (ACID transactions, time travel)
- CSV/JSON (exports and integration)

### 5. **Enterprise-Grade Utilities**
- YAML-based configuration management
- Structured logging with metrics
- Optimized Spark session management

---

## Setup

### Prerequisites
- Python 3.8+
- Apache Spark 3.3+
- Databricks Runtime (optional)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wibnudixon/databricks-data-pipeline.git
   cd databricks-data-pipeline
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the pipeline**:
   Edit `config/pipeline_config.yaml` to set your data sources and outputs.

---

## Usage

### Using the Pipeline Orchestrator

```python
from src.pipeline import DataPipeline

# Initialize pipeline
pipeline = DataPipeline(config_path="config/pipeline_config.yaml")

# Run simple pipeline
pipeline.run_simple_pipeline(
    input_path="data/input/sample_data.csv",
    output_path="data/output/bronze",
    format="csv"
)

# Run complex pipeline with validation
pipeline.run_complex_pipeline(
    input_path="data/input/sample_data.csv",
    output_path="data/output/silver",
    format="csv",
    validate=True
)
```

### Using Individual Modules

**Data Ingestion**:
```python
from src.ingestion import ingest_data_simple, ingest_data_with_schema, get_complex_employee_schema

# Simple ingestion
df = ingest_data_simple("data/input/sample_data.csv", format="csv")

# Schema-enforced ingestion
schema = get_complex_employee_schema()
df = ingest_data_with_schema("data/input/sample_data.csv", schema, format="csv")
```

**Data Transformation**:
```python
from src.transformation import transform_data, flatten_nested_fields

# Apply transformations
df_transformed = transform_data(df)
```

**Data Validation**:
```python
from src.validation import DataQualityValidator

validator = DataQualityValidator("config/data_quality_rules.yaml")
results = validator.run_validation(df, "employee_data")
report = validator.generate_quality_report(results)
```

**Write Data**:
```python
from src.writers import write_data, write_delta_table

# Write as Parquet
write_data(df, "data/output/bronze", format="parquet")

# Write as Delta
write_delta_table(df, "data/output/gold/employees", partition_by=["department"])
```

---

## Branch Integration Summary

This unified architecture incorporates features from all branches:

| Feature | Source Branch | Status |
|---------|--------------|--------|
| Simple Ingestion | complex-schema-enhancements | ✅ Integrated |
| Schema-Enforced Ingestion | main, copilot/manage-repository-branches | ✅ Integrated |
| Data Quality Validator | main, copilot/manage-repository-branches | ✅ Integrated |
| Config Reader | main, copilot/manage-repository-branches | ✅ Integrated |
| Advanced Spark Utils | main, copilot/manage-repository-branches | ✅ Integrated |
| Logging Framework | main, copilot/manage-repository-branches | ✅ Integrated |
| Basic Transformations | main | ✅ Integrated |
| Advanced Transformations | New | ✅ Added |
| Delta Lake Support | Enhanced | ✅ Added |
| Pipeline Orchestrator | New | ✅ Added |

---

## Version History

- **v1.0.0** (Current): Unified architecture integrating all branch features
  - Modular structure with separate components
  - Dual ingestion modes (simple and schema-enforced)
  - Comprehensive data quality framework
  - Configuration-driven pipeline execution
  - Delta Lake and Parquet support
  - Production-ready logging and monitoring
