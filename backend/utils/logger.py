import logging
import sys
from config import settings

def setup_logging():
    """Configure logging for the application"""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    root_logger.addHandler(console_handler)
    
    # Configure specific loggers
    loggers = [
        'agents',
        'tools', 
        'api',
        'main'
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    logging.info("Logging configured successfully")

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger for a module"""
    return logging.getLogger(name) 