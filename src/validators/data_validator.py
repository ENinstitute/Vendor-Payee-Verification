"""
Data Validator
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

from typing import Dict, List, Optional, Tuple
import re

from config.settings import settings
from src.utils.logger import get_logger
from src.validators.iban_validator import iban_validator

logger = get_logger(__name__)


class DataValidator:
    """Validates extracted data quality and consistency"""
    
    def __init__(self):
        self.min_confidence = settings.MIN_CONFIDENCE_THRESHOLD
        self.max_confidence = settings.MAX_CONFIDENCE_THRESHOLD
    
    def validate_extraction(self, vendor_id: str, iban: str, account_name: str, 
                          confidence_score: float) -> Tuple[bool, List[str]]:
        """
        Validate complete extraction result
        
        Args:
            vendor_id: Vendor identifier
            iban: Extracted IBAN
            account_name: Extracted account name
            confidence_score: AI confidence score
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate vendor_id
        if not vendor_id or not vendor_id.strip():
            errors.append("Vendor ID is empty")
        
        # Validate IBAN
        is_valid_iban, _, iban_error = iban_validator.validate(iban)
        if not is_valid_iban:
            errors.append(f"IBAN validation failed: {iban_error}")
        
        # Validate account name
        if not self.validate_account_name(account_name):
            errors.append("Account name is invalid or empty")
        
        # Validate confidence score
        if not self.validate_confidence_score(confidence_score):
            errors.append(f"Confidence score {confidence_score} is below threshold {self.min_confidence}")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"Extraction validation successful for vendor {vendor_id}")
        else:
            logger.warning(f"Extraction validation failed for vendor {vendor_id}: {'; '.join(errors)}")
        
        return is_valid, errors
    
    def validate_account_name(self, account_name: str) -> bool:
        """
        Validate account name/identifier
        
        Args:
            account_name: Account name string
        
        Returns:
            True if valid
        """
        if not account_name or not account_name.strip():
            return False
        
        # Check minimum length
        if len(account_name.strip()) < 2:
            return False
        
        # Check if it contains at least one letter or number
        if not re.search(r'[a-zA-Z0-9]', account_name):
            return False
        
        return True
    
    def validate_confidence_score(self, score: float) -> bool:
        """
        Validate confidence score is within acceptable range
        
        Args:
            score: Confidence score (0.0 to 1.0)
        
        Returns:
            True if score meets minimum threshold
        """
        return self.min_confidence <= score <= 1.0
    
    def get_confidence_level(self, score: float) -> str:
        """
        Get confidence level category
        
        Args:
            score: Confidence score (0.0 to 1.0)
        
        Returns:
            Confidence level string: 'high', 'medium', 'low'
        """
        if score >= self.max_confidence:
            return 'high'
        elif score >= self.min_confidence:
            return 'medium'
        else:
            return 'low'
    
    def validate_batch_consistency(self, extractions: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Validate consistency across a batch of extractions
        
        Args:
            extractions: List of extraction dictionaries
        
        Returns:
            Dictionary with 'valid' and 'invalid' lists
        """
        valid_extractions = []
        invalid_extractions = []
        
        for extraction in extractions:
            is_valid, errors = self.validate_extraction(
                extraction.get('vendor_id', ''),
                extraction.get('iban', ''),
                extraction.get('account_name', ''),
                extraction.get('confidence_score', 0.0)
            )
            
            if is_valid:
                valid_extractions.append(extraction)
            else:
                extraction['validation_errors'] = errors
                invalid_extractions.append(extraction)
        
        logger.info(f"Batch validation: {len(valid_extractions)} valid, {len(invalid_extractions)} invalid")
        
        return {
            'valid': valid_extractions,
            'invalid': invalid_extractions
        }
    
    def detect_duplicate_iban(self, iban: str, existing_extractions: List[Dict]) -> bool:
        """
        Check if IBAN already exists in extractions
        
        Args:
            iban: IBAN to check
            existing_extractions: List of existing extractions
        
        Returns:
            True if duplicate found
        """
        iban_clean = iban.replace(' ', '').upper()
        
        for extraction in existing_extractions:
            existing_iban = extraction.get('iban', '').replace(' ', '').upper()
            if existing_iban == iban_clean:
                logger.warning(f"Duplicate IBAN detected: {iban_clean}")
                return True
        
        return False
    
    def validate_pattern_change(self, vendor_id: str, new_iban: str, 
                               previous_iban: Optional[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate if IBAN change for a vendor is suspicious
        
        Args:
            vendor_id: Vendor identifier
            new_iban: New extracted IBAN
            previous_iban: Previously stored IBAN
        
        Returns:
            Tuple of (should_alert, alert_message)
        """
        if not previous_iban:
            return False, None
        
        new_iban_clean = new_iban.replace(' ', '').upper()
        previous_iban_clean = previous_iban.replace(' ', '').upper()
        
        if new_iban_clean != previous_iban_clean:
            # Check if country codes match
            new_country = new_iban_clean[:2]
            previous_country = previous_iban_clean[:2]
            
            alert_msg = f"IBAN change detected for vendor {vendor_id}: {previous_country}*** -> {new_country}***"
            
            if new_country != previous_country:
                logger.critical(f"Country code change detected: {alert_msg}")
                return True, alert_msg
            else:
                logger.warning(f"IBAN change detected: {alert_msg}")
                return True, alert_msg
        
        return False, None


# Global validator instance
data_validator = DataValidator()
