"""
Pytest Configuration
AI-Powered IBAN Extraction System
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
from config.settings import settings


@pytest.fixture
def db_manager():
    """Fixture for database manager"""
    # Use SQLite for testing
    settings.DB_TYPE = "sqlite"
    settings.SQLITE_DB_PATH = ":memory:"
    
    manager = DatabaseManager()
    manager.initialize_database()
    
    yield manager


@pytest.fixture
def sample_iban():
    """Fixture for valid IBAN"""
    return "IE29AIBK93115212345678"


@pytest.fixture
def sample_extraction():
    """Fixture for sample extraction data"""
    return {
        'vendor_id': 'VEND001',
        'iban': 'IE29AIBK93115212345678',
        'account_name': 'Test Vendor Account',
        'confidence_score': 0.95
    }
