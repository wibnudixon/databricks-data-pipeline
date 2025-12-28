# Migration Guide

## Migrating from Legacy Files to New Architecture

This guide helps you transition from the root-level Python files to the new modular structure.

### Quick Reference

| Legacy File | New Location | Notes |
|------------|--------------|-------|
| `ingestion.py` | `src/ingestion/schema_ingestion.py` | Schema-enforced version |
| | `src/ingestion/simple_ingestion.py` | Simple flexible version |
| `transformation.py` | `src/transformation/basic_transformations.py` | Basic transforms |
| | `src/transformation/advanced_transformations.py` | Advanced transforms |
| `write_data.py` | `src/writers/data_writer.py` | Enhanced with Delta support |
| `data_validator.py` | `src/validation/data_quality_validator.py` | Same functionality |
| `config_reader.py` | `src/utils/config_reader.py` | Same functionality |
| `logger.py` | `src/utils/logger.py` | Same functionality |
| `spark_utils.py` | `src/utils/spark_manager.py` | Same functionality |
| `utils.py` | Deprecated | Use specific utils modules |
| `sample_data.csv` | `data/input/sample_data.csv` | Moved to data directory |

### Code Migration Examples

#### Before (Legacy)
```python
from ingestion import ingest_data
from transformation import transform_data
from write_data import write_data

df = ingest_data("sample_data.csv", format="csv")
df_transformed = transform_data(df)
write_data(df_transformed, "output/data", format="parquet")
```

#### After (New Architecture - Option 1: Using Pipeline Orchestrator)
```python
from src.pipeline import DataPipeline

pipeline = DataPipeline()
pipeline.run_complex_pipeline(
    input_path="data/input/sample_data.csv",
    output_path="data/output/processed",
    format="csv"
)
```

#### After (New Architecture - Option 2: Using Individual Modules)
```python
from src.ingestion import ingest_data_with_schema, get_complex_employee_schema
from src.transformation import transform_data
from src.writers import write_data

schema = get_complex_employee_schema()
df = ingest_data_with_schema("data/input/sample_data.csv", schema, format="csv")
df_transformed = transform_data(df)
write_data(df_transformed, "data/output/processed", format="parquet")
```

### Import Changes

#### Legacy Imports
```python
from ingestion import ingest_data
from transformation import transform_data
from write_data import write_data
from data_validator import DataQualityValidator
from config_reader import ConfigReader
from logger import PipelineLogger
from spark_utils import SparkSessionManager
```

#### New Imports
```python
# For pipeline orchestration (recommended)
from src.pipeline import DataPipeline

# For individual components
from src.ingestion import ingest_data_simple, ingest_data_with_schema, get_complex_employee_schema
from src.transformation import transform_data, flatten_nested_fields
from src.writers import write_data, write_delta_table
from src.validation import DataQualityValidator
from src.utils import ConfigReader, PipelineLogger, SparkSessionManager
```

### Configuration Migration

#### Before
No configuration files; hardcoded parameters in code.

#### After
Use YAML configuration files:

1. **Pipeline Configuration** (`config/pipeline_config.yaml`):
   - Define data sources
   - Configure outputs
   - Set Spark parameters

2. **Data Quality Rules** (`config/data_quality_rules.yaml`):
   - Define validation rules
   - Specify quality thresholds

### Directory Structure Changes

#### Before
```
databricks-data-pipeline/
├── ingestion.py
├── transformation.py
├── write_data.py
├── data_validator.py
├── config_reader.py
├── logger.py
├── spark_utils.py
├── utils.py
└── sample_data.csv
```

#### After
```
databricks-data-pipeline/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   ├── writers/
│   ├── utils/
│   └── pipeline.py
├── config/
│   ├── pipeline_config.yaml
│   └── data_quality_rules.yaml
├── data/
│   ├── input/
│   └── output/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md

# Legacy files kept for backward compatibility
├── ingestion.py
├── transformation.py
├── write_data.py
├── data_validator.py
├── config_reader.py
├── logger.py
├── spark_utils.py
└── utils.py
```

### Feature Enhancements

#### New Features Not in Legacy Code

1. **Pipeline Orchestrator** (`src/pipeline.py`):
   - End-to-end workflow management
   - Multiple pipeline types (simple, complex, delta)

2. **Simple Ingestion** (`src/ingestion/simple_ingestion.py`):
   - Flexible schema-less ingestion
   - From complex-schema-enhancements branch

3. **Advanced Transformations** (`src/transformation/advanced_transformations.py`):
   - Complex field extraction
   - Array/Map operations

4. **Delta Lake Support** (`src/writers/data_writer.py`):
   - `write_delta_table()` function
   - Optimized writes and auto-compaction

5. **Configuration Management**:
   - YAML-based configuration
   - Centralized settings

### Backward Compatibility

The legacy files remain in the root directory for backward compatibility. However:
- They are **not updated** with new features
- They may be **removed in future versions**
- **Migration to the new structure is recommended**

### Step-by-Step Migration

1. **Review the new structure**: Familiarize yourself with the `src/` directory layout
2. **Update imports**: Change from root-level imports to `src.*` imports
3. **Add configuration**: Create `config/pipeline_config.yaml` for your pipeline
4. **Update data paths**: Move data to `data/input/` and set outputs to `data/output/`
5. **Test**: Run your pipeline with the new structure
6. **Remove legacy imports**: Once verified, remove old import statements

### Common Issues and Solutions

#### Issue: Import errors with new structure
**Solution**: Ensure the project root is in your Python path:
```python
import sys
sys.path.insert(0, '/path/to/databricks-data-pipeline')
```

Or set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/databricks-data-pipeline:$PYTHONPATH
```

#### Issue: Configuration file not found
**Solution**: Provide absolute path or ensure working directory is project root:
```python
pipeline = DataPipeline(config_path="/absolute/path/to/config/pipeline_config.yaml")
```

#### Issue: Legacy code still references old files
**Solution**: Use the legacy files as-is (they still work) or migrate incrementally, module by module.

### Benefits of Migration

1. **Better Organization**: Modular structure with clear separation of concerns
2. **Easier Maintenance**: Changes isolated to specific modules
3. **Enhanced Features**: Access to new capabilities (Delta Lake, pipeline orchestrator)
4. **Configuration-Driven**: Easier to adapt to different environments
5. **Better Documentation**: Each module has clear purpose and documentation

### Need Help?

- Review `README.md` for architecture overview
- Check `docs/ARCHITECTURE.md` for detailed component information
- Examine `src/pipeline.py` for usage examples
