import logging
import sys
from datetime import datetime

class PipelineLogger:
    """Custom logger for data pipeline operations."""
    
    def __init__(self, name, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Formatter
        formatter = logging. Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger

def log_pipeline_metrics(stage, records_processed, duration, status):
    """Log pipeline execution metrics."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "records_processed": records_processed,
        "duration_seconds": duration,
        "status": status
    }
    return metrics