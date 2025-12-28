"""
Ingestion module for loading data from various sources.
"""
from .simple_ingestion import ingest_data_simple
from .schema_ingestion import ingest_data_with_schema, get_complex_employee_schema

__all__ = [
    'ingest_data_simple',
    'ingest_data_with_schema',
    'get_complex_employee_schema'
]
