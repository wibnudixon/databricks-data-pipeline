import logging


def setup_logging():
    """
    Setup logging for the pipeline.

    Returns:
        Logger: Configured logger.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    return logging.getLogger(__name__)