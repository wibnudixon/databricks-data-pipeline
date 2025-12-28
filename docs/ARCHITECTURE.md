# Architecture Documentation

## Overview

This document describes the architecture of the Databricks Data Pipeline project, including design decisions, module organization, and data flow.

## Design Principles

1. **Modularity**: Each component has a single responsibility and can be used independently
2. **Configuration-Driven**: Behavior is controlled through YAML configurations, not hardcoded
3. **Extensibility**: Easy to add new data sources, transformations, or validation rules
4. **Observability**: Built-in logging and metrics for monitoring pipeline health
5. **Quality-First**: Data quality validation is a core part of the pipeline

## System Architecture

### High-Level Architecture

```
┌─────────────────┐
│  Configuration  │
│   (YAML Files)  │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────┐
│                    Run Pipeline                          │
│  (Orchestrates the complete data flow)                   │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Ingestion   │→│Transformation│→│ Write Data   │
│   (Bronze)   │ │   (Silver)   │ │   (Gold)     │
└──────────────┘ └──────────────┘ └──────────────┘
        ↓               ↓               ↓
┌─────────────────────────────────────────────┐
│           Utility Services                   │
│  • Logging                                   │
│  • Spark Session Management                 │
│  • Data Quality Validation                  │
│  • Configuration Management                 │
└─────────────────────────────────────────────┘
```

## Module Structure

### Core Pipeline Modules (`src/pipeline/`)

#### 1. Ingestion Module (`ingestion.py`)
**Purpose**: Load raw data from various sources with schema enforcement

**Key Features**:
- Multi-format support (CSV, JSON, Parquet)
- Schema enforcement with complex types (structs, arrays, maps)
- Handles nested data structures

**Usage**:
```python
df = ingest_data(file_path="data/input.csv", format="csv")
```

#### 2. Transformation Module (`transformation.py`)
**Purpose**: Clean, enrich, and transform data

**Key Features**:
- Flattening nested structures
- Calculated fields (tenure, compensation, etc.)
- Array/map operations
- Data aggregations

**Usage**:
```python
df_transformed = transform_data(df)
```

#### 3. Write Data Module (`write_data.py`)
**Purpose**: Persist processed data to storage

**Key Features**:
- Multi-format output (Parquet, Delta, CSV)
- Partitioning support
- Overwrite/append modes

**Usage**:
```python
write_data(df, output_path, format="delta", partition_by=["year", "month"])
```

### Utility Modules (`src/utils/`)

#### 1. Configuration Reader (`config_reader.py`)
**Purpose**: Centralized configuration management

**Features**:
- YAML-based configuration
- Dot notation access (`config.get("paths.bronze")`)
- Source-specific configuration retrieval

#### 2. Data Quality Validator (`data_validator.py`)
**Purpose**: Ensure data quality through configurable rules

**Supported Validations**:
- Not null checks
- Uniqueness checks
- Range validation
- Format validation (regex)
- Allowed values validation

**Usage**:
```python
validator = DataQualityValidator("config/data_quality_rules.yaml")
results = validator.run_validation(df, "employee_data")
report = validator.generate_quality_report(results)
```

#### 3. Logger (`logger.py`)
**Purpose**: Structured logging for pipeline operations

**Features**:
- Customizable log levels
- Timestamped entries
- Metrics tracking (records processed, duration, status)

#### 4. Spark Utilities (`spark_utils.py`)
**Purpose**: Spark session management and schema definitions

**Features**:
- Optimized Spark configuration
- Pre-defined schemas for common data types
- Singleton session management

#### 5. General Utilities (`utils.py`)
**Purpose**: Common utility functions

## Data Flow

### Bronze → Silver → Gold Pattern

```
┌─────────────┐
│   Bronze    │  Raw data as-is from source
│  (Ingestion)│  - Schema enforcement
└──────┬──────┘  - Basic validation
       │
       ↓
┌─────────────┐
│   Silver    │  Cleaned and enriched data
│(Transformation)│  - Flattened structures
└──────┬──────┘  - Calculated fields
       │         - Type conversions
       ↓
┌─────────────┐
│    Gold     │  Analytics-ready data
│ (Write Data)│  - Quality validated
└─────────────┘  - Optimized storage

```

### Validation Flow

```
Data → Validation Rules → Quality Checks → Report
                              ↓
                         Pass/Fail
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              Continue Pipeline    Alert/Stop
```

## Configuration Management

### Pipeline Configuration (`pipeline_config.yaml`)

Defines:
- Data paths (bronze, silver, gold)
- Source configurations
- Output settings
- Spark configurations
- Processing parameters

### Data Quality Rules (`data_quality_rules.yaml`)

Defines:
- Dataset-specific validation rules
- Column-level checks
- Validation thresholds

## Extensibility Points

### Adding a New Data Source

1. Add source configuration to `pipeline_config.yaml`
2. Optionally create a custom schema in `spark_utils.py`
3. Use existing `ingest_data` function or extend it

### Adding a New Transformation

1. Add transformation logic to `transformation.py`
2. Update `transform_data` function or create a new transformation function
3. Chain transformations as needed

### Adding New Validation Rules

1. Add rule definition to `data_quality_rules.yaml`
2. If needed, implement new validation type in `data_validator.py`
3. Run validation as part of pipeline

## Best Practices

### 1. Schema Management
- Define schemas explicitly for all data sources
- Use appropriate data types (avoid strings for everything)
- Handle nested structures properly

### 2. Error Handling
- Use try-except blocks for I/O operations
- Log errors with context
- Fail fast on critical errors

### 3. Performance
- Use appropriate Spark configurations
- Partition data strategically
- Cache dataframes when reused
- Minimize shuffles

### 4. Testing
- Test individual modules in isolation
- Use small sample datasets for unit tests
- Implement integration tests for end-to-end flow

### 5. Configuration
- Keep environment-specific configs separate
- Use version control for configurations
- Document all configuration options

## Deployment Options

### Local Development
```bash
python run_pipeline.py --input data/sample.csv --output output/
```

### Databricks Notebook
```python
%run ./run_pipeline
run_pipeline(config_path="/dbfs/config/pipeline_config.yaml")
```

### Databricks Job
- Package as a wheel or egg
- Configure job with required libraries
- Schedule using Databricks Jobs

### Azure Data Factory / AWS Glue
- Use as custom activity
- Pass configurations via environment variables
- Monitor through native platform tools

## Monitoring and Observability

### Logging
- All pipeline stages log start/completion
- Record counts logged at each stage
- Errors logged with full traceback

### Metrics
- Records processed
- Processing duration
- Success/failure rates
- Data quality scores

## Future Enhancements

1. **Streaming Support**: Add streaming ingestion capabilities
2. **Schema Evolution**: Handle schema changes automatically
3. **Data Lineage**: Track data provenance through the pipeline
4. **Advanced Monitoring**: Integrate with monitoring tools (Prometheus, Grafana)
5. **Testing Framework**: Comprehensive unit and integration tests
6. **CI/CD**: Automated testing and deployment pipelines
