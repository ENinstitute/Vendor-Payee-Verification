"""
Configuration Settings
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    """Application configuration settings"""
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"
    
    # Anthropic API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    ANTHROPIC_MAX_TOKENS: int = 4096
    ANTHROPIC_TEMPERATURE: float = 0.0  # Deterministic for extraction
    
    # Database Configuration
    DB_TYPE: str = os.getenv("DB_TYPE", "postgresql")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "iban_extraction")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", str(BASE_DIR / "database" / "iban_extraction.db"))
    
    @property
    def DATABASE_URL(self) -> str:
        """Generate database URL based on DB_TYPE"""
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        else:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Application Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_CONFIDENCE_THRESHOLD: float = float(os.getenv("MAX_CONFIDENCE_THRESHOLD", "0.90"))
    MIN_CONFIDENCE_THRESHOLD: float = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.70"))
    PROCESSING_TIMEOUT: int = int(os.getenv("PROCESSING_TIMEOUT", "30"))
    
    # Security Settings
    ENCRYPTION_KEY: Optional[str] = os.getenv("ENCRYPTION_KEY")
    ALERT_THRESHOLD_PATTERN_CHANGE: float = float(os.getenv("ALERT_THRESHOLD_PATTERN_CHANGE", "0.80"))
    
    # Azure Storage Configuration
    AZURE_STORAGE_ACCOUNT: str = os.getenv("AZURE_STORAGE_ACCOUNT", "")
    AZURE_STORAGE_KEY: str = os.getenv("AZURE_STORAGE_KEY", "")
    AZURE_CONTAINER_NAME: str = os.getenv("AZURE_CONTAINER_NAME", "iban-extractions")
    
    # File Processing
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    SUPPORTED_FORMATS: List[str] = os.getenv("SUPPORTED_FORMATS", "pdf,jpg,jpeg,png,tiff").split(",")
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "50"))
    
    # Directories
    DATA_DIR: Path = BASE_DIR / "data"
    INVOICES_TRAINING_DIR: Path = DATA_DIR / "invoices" / "training"
    INVOICES_PROCESSING_DIR: Path = DATA_DIR / "invoices" / "processing"
    PATTERNS_DIR: Path = DATA_DIR / "patterns"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Dynamics GP Configuration
    DYNAMICS_GP_HOST: str = os.getenv("DYNAMICS_GP_HOST", "")
    DYNAMICS_GP_DB: str = os.getenv("DYNAMICS_GP_DB", "")
    DYNAMICS_GP_USER: str = os.getenv("DYNAMICS_GP_USER", "")
    DYNAMICS_GP_PASSWORD: str = os.getenv("DYNAMICS_GP_PASSWORD", "")
    
    @property
    def DYNAMICS_GP_CONNECTION_STRING(self) -> str:
        """Generate Dynamics GP connection string"""
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.DYNAMICS_GP_HOST};"
            f"DATABASE={self.DYNAMICS_GP_DB};"
            f"UID={self.DYNAMICS_GP_USER};"
            f"PWD={self.DYNAMICS_GP_PASSWORD}"
        )
    
    # Email Notifications
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.office365.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_TO: List[str] = os.getenv(
        "ALERT_EMAIL_TO", 
        "kieran.daly@charteredaccountants.ie"
    ).split(",")
    
    # IBAN Validation Settings
    IBAN_COUNTRY_CODES: List[str] = ["IE", "GB", "DE", "FR", "ES", "IT", "NL", "BE"]  # Expandable
    
    # Pattern Recognition Settings
    PATTERN_SIMILARITY_THRESHOLD: float = 0.85
    MAX_PATTERNS_PER_VENDOR: int = 3
    
    # CSV Export Settings
    CSV_ENCODING: str = "utf-8"
    CSV_DELIMITER: str = ","
    CSV_COLUMNS: List[str] = ["vendor_id", "iban", "account_name", "confidence_score"]
    
    # Performance Settings
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    CHUNK_SIZE: int = 1000
    
    def __init__(self):
        """Initialize settings and create necessary directories"""
        self._create_directories()
        self._validate_settings()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.INVOICES_TRAINING_DIR,
            self.INVOICES_PROCESSING_DIR,
            self.PATTERNS_DIR,
            self.OUTPUT_DIR,
            self.LOGS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _validate_settings(self):
        """Validate critical settings"""
        if not self.ANTHROPIC_API_KEY and self.ENV == "production":
            raise ValueError("ANTHROPIC_API_KEY must be set in production environment")
        
        if self.DB_TYPE == "postgresql" and not all([self.DB_USER, self.DB_PASSWORD]):
            raise ValueError("Database credentials must be set for PostgreSQL")
        
        if self.MAX_CONFIDENCE_THRESHOLD <= self.MIN_CONFIDENCE_THRESHOLD:
            raise ValueError("MAX_CONFIDENCE_THRESHOLD must be greater than MIN_CONFIDENCE_THRESHOLD")


# Global settings instance
settings = Settings()
