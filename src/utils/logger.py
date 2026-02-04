"""
Logging Utility
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import colorlog

from config.settings import settings


def get_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (typically __name__)
        log_file: Optional specific log file name
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create logs directory if it doesn't exist
    log_dir = settings.LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Console Handler with colors
    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File Handler
    if log_file is None:
        log_file = f"iban_extraction_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_path = log_dir / log_file
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


class ExtractionLogger:
    """Specialized logger for extraction operations"""
    
    def __init__(self, db_manager, extraction_id: Optional[int] = None):
        self.db_manager = db_manager
        self.extraction_id = extraction_id
        self.logger = get_logger(self.__class__.__name__)
    
    def log(self, level: str, message: str, data: Optional[dict] = None):
        """Log message to both file and database"""
        # Log to file
        log_method = getattr(self.logger, level.lower())
        log_method(message)
        
        # Log to database if extraction_id is set
        if self.extraction_id and self.db_manager:
            try:
                with self.db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO extraction_logs (extraction_id, log_level, log_message, log_data)
                        VALUES (?, ?, ?, ?)
                        """ if settings.DB_TYPE == "sqlite" else
                        """
                        INSERT INTO extraction_logs (extraction_id, log_level, log_message, log_data)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (self.extraction_id, level.upper(), message, str(data) if data else None)
                    )
                    cursor.close()
            except Exception as e:
                self.logger.error(f"Failed to log to database: {str(e)}")
    
    def debug(self, message: str, data: Optional[dict] = None):
        self.log('DEBUG', message, data)
    
    def info(self, message: str, data: Optional[dict] = None):
        self.log('INFO', message, data)
    
    def warning(self, message: str, data: Optional[dict] = None):
        self.log('WARNING', message, data)
    
    def error(self, message: str, data: Optional[dict] = None):
        self.log('ERROR', message, data)
    
    def critical(self, message: str, data: Optional[dict] = None):
        self.log('CRITICAL', message, data)
