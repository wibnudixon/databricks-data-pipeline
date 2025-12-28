from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, isnan, isnull, regexp_extract
import yaml
from pathlib import Path

class DataQualityValidator:
    """Validate data quality based on configurable rules."""
    
    def __init__(self, rules_path="config/data_quality_rules.yaml"):
        self.rules = self._load_rules(rules_path)
        self.validation_results = []
    
    def _load_rules(self, rules_path):
        """Load data quality rules from YAML."""
        with open(rules_path, 'r') as file:
            return yaml.safe_load(file)
    
    def validate_not_null(self, df: DataFrame, column: str) -> dict:
        """Check for null values in a column."""
        total_count = df.count()
        null_count = df.filter(col(column).isNull()).count()
        
        return {
            "check": "not_null",
            "column": column,
            "passed": null_count == 0,
            "null_count": null_count,
            "null_percentage": (null_count / total_count * 100) if total_count > 0 else 0
        }
    
    def validate_unique(self, df: DataFrame, column: str) -> dict:
        """Check for duplicate values in a column."""
        total_count = df.count()
        distinct_count = df.select(column).distinct().count()
        
        return {
            "check": "unique",
            "column": column,
            "passed": total_count == distinct_count,
            "duplicate_count": total_count - distinct_count
        }
    
    def validate_range(self, df: DataFrame, column: str, min_val: float, max_val: float) -> dict:
        """Check if values are within specified range."""
        out_of_range = df.filter(
            (col(column) < min_val) | (col(column) > max_val)
        ).count()
        
        return {
            "check": "range",
            "column": column,
            "passed": out_of_range == 0,
            "out_of_range_count": out_of_range,
            "range": f"{min_val} - {max_val}"
        }
    
    def validate_format(self, df: DataFrame, column: str, pattern: str) -> dict:
        """Check if values match a regex pattern."""
        invalid_format = df.filter(
            ~col(column).rlike(pattern)
        ).count()
        
        return {
            "check": "format",
            "column": column,
            "passed": invalid_format == 0,
            "invalid_count": invalid_format,
            "pattern": pattern
        }
    
    def validate_allowed_values(self, df: DataFrame, column: str, allowed_values: list) -> dict:
        """Check if values are in allowed list."""
        invalid_values = df.filter(
            ~col(column).isin(allowed_values)
        ).count()
        
        return {
            "check": "allowed_values",
            "column": column,
            "passed": invalid_values == 0,
            "invalid_count": invalid_values,
            "allowed_values": allowed_values
        }
    
    def run_validation(self, df: DataFrame, dataset_name: str) -> list:
        """Run all validation rules for a dataset."""
        results = []
        
        if dataset_name not in self.rules.get('rules', {}):
            return results
        
        for rule in self.rules['rules'][dataset_name]:
            column = rule['column']
            
            for check in rule['checks']:
                check_type = check['type']
                
                if check_type == 'not_null':
                    result = self.validate_not_null(df, column)
                elif check_type == 'unique':
                    result = self.validate_unique(df, column)
                elif check_type == 'range':
                    result = self.validate_range(df, column, check['min'], check['max'])
                elif check_type == 'format':
                    result = self.validate_format(df, column, check['pattern'])
                elif check_type == 'allowed_values':
                    result = self.validate_allowed_values(df, column, check['values'])
                else:
                    continue
                
                results.append(result)
        
        return results
    
    def generate_quality_report(self, results: list) -> dict:
        """Generate summary report of data quality checks."""
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r['passed'])
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "success_rate": (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            "details": results
        }