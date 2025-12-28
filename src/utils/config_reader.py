import yaml
from pathlib import Path

class ConfigReader:
    """Read and manage pipeline configuration."""
    
    def __init__(self, config_path="config/pipeline_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self):
        """Load YAML configuration file."""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")
    
    def get(self, key_path, default=None):
        """
        Get configuration value using dot notation.
        Example: config.get('paths.bronze')
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        
        return value if value is not None else default
    
    def get_source_config(self, source_name):
        """Get configuration for a specific data source."""
        return self.config.get('sources', {}).get(source_name, {})