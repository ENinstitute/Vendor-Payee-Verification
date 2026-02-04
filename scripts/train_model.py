"""
Training Script
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import train_model

if __name__ == "__main__":
    train_model()
