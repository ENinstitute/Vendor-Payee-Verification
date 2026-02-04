"""
IBAN Validator Unit Tests
AI-Powered IBAN Extraction System
"""

import pytest
from src.validators.iban_validator import IBANValidator


class TestIBANValidator:
    """Test cases for IBAN Validator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.validator = IBANValidator()
    
    def test_valid_irish_iban(self):
        """Test validation of valid Irish IBAN"""
        iban = "IE29AIBK93115212345678"
        is_valid, formatted, error = self.validator.validate(iban)
        
        assert is_valid is True
        assert formatted is not None
        assert error is None
    
    def test_valid_uk_iban(self):
        """Test validation of valid UK IBAN"""
        iban = "GB82WEST12345698765432"
        is_valid, formatted, error = self.validator.validate(iban)
        
        assert is_valid is True
        assert formatted is not None
        assert error is None
    
    def test_invalid_iban_checksum(self):
        """Test validation of IBAN with invalid checksum"""
        iban = "IE00AIBK93115212345678"  # Invalid checksum
        is_valid, formatted, error = self.validator.validate(iban)
        
        assert is_valid is False
        assert formatted is None
        assert error is not None
    
    def test_empty_iban(self):
        """Test validation of empty IBAN"""
        is_valid, formatted, error = self.validator.validate("")
        
        assert is_valid is False
        assert error == "IBAN is empty"
    
    def test_invalid_iban_format(self):
        """Test validation of invalid IBAN format"""
        iban = "INVALID123"
        is_valid, formatted, error = self.validator.validate(iban)
        
        assert is_valid is False
        assert "Invalid IBAN format" in error
    
    def test_iban_too_short(self):
        """Test validation of IBAN that's too short"""
        iban = "IE12345"
        is_valid, formatted, error = self.validator.validate(iban)
        
        assert is_valid is False
        assert "Invalid IBAN length" in error
    
    def test_extract_country_code(self):
        """Test extracting country code from IBAN"""
        iban = "IE29AIBK93115212345678"
        country = self.validator.extract_country_code(iban)
        
        assert country == "IE"
    
    def test_format_iban(self):
        """Test IBAN formatting with spaces"""
        iban = "IE29AIBK93115212345678"
        formatted = self.validator.format_iban(iban)
        
        assert " " in formatted
        assert "IE29" in formatted
    
    def test_iban_with_spaces(self):
        """Test validation of IBAN with spaces"""
        iban = "IE29 AIBK 9311 5212 3456 78"
        is_valid, formatted, error = self.validator.validate(iban)
        
        assert is_valid is True
        assert " " not in formatted  # Should remove spaces
