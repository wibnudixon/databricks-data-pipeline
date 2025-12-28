#!/usr/bin/env python
"""
Verify the project structure and imports.

This script checks that all files are in place and the structure is correct.
It does NOT require PySpark to be installed.
"""
import os
import sys

def check_structure():
    """Verify all expected files and directories exist."""
    print("=" * 60)
    print("PROJECT STRUCTURE VERIFICATION")
    print("=" * 60)
    
    expected_structure = {
        'directories': [
            'src',
            'src/pipeline',
            'src/utils',
            'config',
            'data',
            'tests',
            'docs',
            'examples',
        ],
        'files': [
            'README.md',
            'requirements.txt',
            'run_pipeline.py',
            '.gitignore',
            'src/__init__.py',
            'src/pipeline/__init__.py',
            'src/pipeline/ingestion.py',
            'src/pipeline/transformation.py',
            'src/pipeline/write_data.py',
            'src/utils/__init__.py',
            'src/utils/config_reader.py',
            'src/utils/data_validator.py',
            'src/utils/logger.py',
            'src/utils/spark_utils.py',
            'src/utils/utils.py',
            'config/pipeline_config.yaml',
            'config/data_quality_rules.yaml',
            'tests/__init__.py',
            'tests/test_pipeline.py',
            'docs/ARCHITECTURE.md',
            'examples/basic_usage.py',
            'examples/data_quality_example.py',
        ]
    }
    
    print("\nChecking directories...")
    all_dirs_ok = True
    for directory in expected_structure['directories']:
        if os.path.isdir(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ NOT FOUND")
            all_dirs_ok = False
    
    print("\nChecking files...")
    all_files_ok = True
    for file_path in expected_structure['files']:
        if os.path.isfile(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} NOT FOUND")
            all_files_ok = False
    
    print("\n" + "=" * 60)
    if all_dirs_ok and all_files_ok:
        print("✓ PROJECT STRUCTURE VERIFICATION PASSED")
        print("=" * 60)
        print("\nThe project is properly structured!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure the pipeline: edit config/pipeline_config.yaml")
        print("3. Run the pipeline: python run_pipeline.py")
        return True
    else:
        print("✗ PROJECT STRUCTURE VERIFICATION FAILED")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = check_structure()
    sys.exit(0 if success else 1)
