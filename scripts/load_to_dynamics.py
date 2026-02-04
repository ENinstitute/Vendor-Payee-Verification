"""
Dynamics GP Loading Script
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import load_to_dynamics

if __name__ == "__main__":
    load_to_dynamics()
