# Architecture Documentation

## Overview
This document provides detailed information about the unified architecture of the Databricks data pipeline.

## Component Details

### 1. Ingestion Layer

#### Simple Ingestion (`src/ingestion/simple_ingestion.py`)
- **Purpose**: Flexible data loading without strict schema enforcement
- **Use Cases**: 
  - Exploratory data analysis
  - Rapidly changing data structures
  - Schema inference scenarios
- **Source**: Adapted from `complex-schema-enhancements` branch

#### Schema-Enforced Ingestion (`src/ingestion/schema_ingestion.py`)
- **Purpose**: Type-safe data loading with predefined schemas
- **Use Cases**:
  - Production pipelines
  - Data quality enforcement
  - Complex nested structures (arrays, maps, structs)
- **Source**: Adapted from `main` and `copilot/manage-repository-branches` branches

### 2. Validation Layer

#### Data Quality Validator (`src/validation/data_quality_validator.py`)
- **Purpose**: Comprehensive data quality checks
- **Validation Types**:
  - Not Null: Ensure required fields have values
  - Unique: Check for duplicate values
  - Range: Validate numeric ranges
  - Format: Regex pattern matching
  - Allowed Values: Enum validation
- **Configuration**: YAML-based rules in `config/data_quality_rules.yaml`
- **Source**: Adapted from `main` branch

### 3. Transformation Layer

#### Basic Transformations (`src/transformation/basic_transformations.py`)
- **Purpose**: Common data transformations
- **Features**:
  - Flatten nested structures
  - Calculate derived metrics
  - Aggregate statistics
- **Source**: Adapted from `main` branch

#### Advanced Transformations (`src/transformation/advanced_transformations.py`)
- **Purpose**: Complex data manipulations
- **Features**:
  - Field extraction from nested structures
  - Array and map operations
  - Custom business logic
- **Source**: New enhancements for unified architecture

### 4. Writers Layer

#### Data Writer (`src/writers/data_writer.py`)
- **Purpose**: Save processed data to various formats
- **Supported Formats**:
  - Parquet: Columnar storage, efficient for analytics
  - Delta Lake: ACID transactions, time travel, versioning
  - CSV/JSON: Exports and integrations
- **Features**:
  - Partitioning support
  - Multiple write modes (overwrite, append, merge)
  - Optimized writes for Delta Lake
- **Source**: Enhanced from `main` branch

### 5. Utilities Layer

#### Config Reader (`src/utils/config_reader.py`)
- **Purpose**: YAML configuration management
- **Features**:
  - Dot notation access
  - Default values
  - Source-specific configurations
- **Source**: From `main` branch

#### Logger (`src/utils/logger.py`)
- **Purpose**: Structured logging for pipeline operations
- **Features**:
  - Configurable log levels
  - Timestamped messages
  - Pipeline metrics tracking
- **Source**: From `main` branch

#### Spark Manager (`src/utils/spark_manager.py`)
- **Purpose**: Optimized Spark session management
- **Features**:
  - Adaptive query execution
  - Delta Lake optimizations
  - Predefined schemas
- **Source**: From `main` branch

## Pipeline Orchestrator

### Main Pipeline (`src/pipeline.py`)
- **Purpose**: Unified orchestration of all components
- **Pipeline Types**:
  1. **Simple Pipeline**: Basic ingestion and writing
  2. **Complex Pipeline**: Full workflow with schema, validation, and transformation
  3. **Delta Pipeline**: Specialized for Delta Lake output
- **Source**: New for unified architecture

## Data Flow

### Bronze Layer (Raw)
1. Data ingestion from source
2. Minimal or no transformations
3. Schema enforcement (optional)
4. Write to Parquet/Delta

### Silver Layer (Cleaned)
1. Load from Bronze
2. Data quality validation
3. Basic transformations
4. Business logic application
5. Write to Delta

### Gold Layer (Analytics-Ready)
1. Load from Silver
2. Advanced transformations
3. Aggregations and feature engineering
4. Optimized for queries
5. Write to Delta with partitioning

## Configuration Management

### Pipeline Configuration (`config/pipeline_config.yaml`)
- Data source definitions
- Output configurations
- Spark settings
- Logging preferences

### Data Quality Rules (`config/data_quality_rules.yaml`)
- Dataset-specific validation rules
- Column-level checks
- Threshold definitions

## Best Practices

1. **Schema Management**:
   - Use schema enforcement for production
   - Version control schema definitions
   - Document schema changes

2. **Validation**:
   - Define quality rules early
   - Monitor validation metrics
   - Alert on quality issues

3. **Performance**:
   - Partition large datasets
   - Use Delta Lake for frequent updates
   - Enable Spark optimizations

4. **Monitoring**:
   - Log all pipeline stages
   - Track record counts
   - Monitor execution times

## Integration Points

### From complex-schema-enhancements Branch
- Simple, flexible ingestion
- Options-based configuration

### From main Branch
- Complex schema support
- Data validation framework
- Comprehensive utilities

### From copilot/manage-repository-branches Branch
- Enhanced documentation
- Configuration examples

### New Enhancements
- Pipeline orchestrator
- Advanced transformations
- Enhanced Delta Lake support
- Comprehensive documentation
