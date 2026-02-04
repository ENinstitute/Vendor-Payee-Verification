"""
IBAN Validator
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import re
from typing import Optional, Tuple
from schwifty import IBAN
from schwifty.exceptions import SchwiftyException

from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class IBANValidator:
    """Validates IBAN format and checksum"""
    
    def __init__(self):
        self.allowed_country_codes = settings.IBAN_COUNTRY_CODES
    
    def validate(self, iban: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate IBAN format and checksum
        
        Args:
            iban: IBAN string to validate
        
        Returns:
            Tuple of (is_valid, formatted_iban, error_message)
        """
        if not iban:
            return False, None, "IBAN is empty"
        
        # Remove whitespace and convert to uppercase
        iban_clean = re.sub(r'\s+', '', iban).upper()
        
        # Basic format check
        if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z0-9]+$', iban_clean):
            return False, None, "Invalid IBAN format"
        
        # Length check (min 15, max 34)
        if len(iban_clean) < 15 or len(iban_clean) > 34:
            return False, None, f"Invalid IBAN length: {len(iban_clean)}"
        
        # Country code check
        country_code = iban_clean[:2]
        if country_code not in self.allowed_country_codes:
            logger.warning(f"IBAN country code {country_code} not in allowed list")
        
        # Validate using schwifty library (includes checksum validation)
        try:
            iban_obj = IBAN(iban_clean)
            formatted_iban = str(iban_obj)
            
            logger.info(f"IBAN validation successful: {country_code}**************")
            return True, formatted_iban, None
            
        except SchwiftyException as e:
            error_msg = f"Invalid IBAN: {str(e)}"
            logger.warning(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"IBAN validation error: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def extract_country_code(self, iban: str) -> Optional[str]:
        """Extract country code from IBAN"""
        iban_clean = re.sub(r'\s+', '', iban).upper()
        if len(iban_clean) >= 2:
            return iban_clean[:2]
        return None
    
    def format_iban(self, iban: str, separator: str = ' ', group_size: int = 4) -> str:
        """
        Format IBAN with separators for readability
        
        Args:
            iban: IBAN string
            separator: Character to use as separator (default: space)
            group_size: Number of characters per group (default: 4)
        
        Returns:
            Formatted IBAN string
        """
        iban_clean = re.sub(r'\s+', '', iban).upper()
        
        # Group characters
        groups = [iban_clean[i:i+group_size] for i in range(0, len(iban_clean), group_size)]
        
        return separator.join(groups)
    
    def is_checksum_valid(self, iban: str) -> bool:
        """
        Verify IBAN checksum
        
        Args:
            iban: IBAN string
        
        Returns:
            True if checksum is valid
        """
        is_valid, _, _ = self.validate(iban)
        return is_valid
    
    @staticmethod
    def calculate_checksum(iban_without_check: str) -> str:
        """
        Calculate IBAN checksum digits
        
        Args:
            iban_without_check: IBAN without check digits (e.g., 'IE00...')
        
        Returns:
            Complete IBAN with valid check digits
        """
        try:
            # Use schwifty to generate valid IBAN
            country_code = iban_without_check[:2]
            account_code = iban_without_check[4:]
            
            iban_obj = IBAN.generate(country_code, bank_code="", account_code=account_code)
            return str(iban_obj)
        except Exception as e:
            logger.error(f"Error calculating checksum: {str(e)}")
            return iban_without_check


# Global validator instance
iban_validator = IBANValidator()
