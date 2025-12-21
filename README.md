# databricks-data-pipeline

## About
This repository demonstrates an end-to-end data pipeline using Databricks, PySpark, and SQL for scalable data engineering.

---

## Pipeline Overview
1. **Data Ingestion**: Load raw data from multiple sources (CSV/JSON/SQL).
2. **Transformation**: Clean and transform data into analytics-ready format.
3. **Writing Data**: Save transformed data in Delta Lake/Parquet format.

---

### Setup
1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Upload scripts to a Databricks workspace or run locally with Spark.
3. Place sample data in the `data/` directory (e.g., `sample_data.csv`).

---

## Running Instructions

### Step 1: Data Ingestion
Run `ingestion.py` script to ingest raw data:
```python
from scripts.ingestion import ingest_data

file_path = "data/sample_data.csv"
df = ingest_data(file_path, format="csv")
df.show()
```

### Step 2: Data Transformation
Run `transformation.py` script to clean and transform the data:
```python
from scripts.transformation import transform_data

df_transformed = transform_data(df)
df_transformed.show()
```

### Step 3: Write Data
Save transformed data using `write_data.py`:
```python
from scripts.write_data import write_data

output_path = "output/data"
write_data(df_transformed, output_path, format="parquet")
```

---

## Files and Directories
- `data/`: Contains sample raw data files.
- `scripts/`: Python scripts for the pipeline.
- `requirements.txt`: Python package dependencies.
- `README.md`: Documentation for setup and usage.
