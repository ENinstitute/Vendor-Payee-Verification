"""
Data Validator Unit Tests
AI-Powered IBAN Extraction System
"""

import pytest
from src.validators.data_validator import DataValidator


class TestDataValidator:
    """Test cases for Data Validator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.validator = DataValidator()
    
    def test_valid_extraction(self):
        """Test validation of valid extraction"""
        is_valid, errors = self.validator.validate_extraction(
            vendor_id="VEND001",
            iban="IE29AIBK93115212345678",
            account_name="Test Account",
            confidence_score=0.95
        )
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_empty_vendor_id(self):
        """Test validation with empty vendor ID"""
        is_valid, errors = self.validator.validate_extraction(
            vendor_id="",
            iban="IE29AIBK93115212345678",
            account_name="Test Account",
            confidence_score=0.95
        )
        
        assert is_valid is False
        assert any("Vendor ID" in error for error in errors)
    
    def test_invalid_iban(self):
        """Test validation with invalid IBAN"""
        is_valid, errors = self.validator.validate_extraction(
            vendor_id="VEND001",
            iban="INVALID123",
            account_name="Test Account",
            confidence_score=0.95
        )
        
        assert is_valid is False
        assert any("IBAN validation failed" in error for error in errors)
    
    def test_low_confidence_score(self):
        """Test validation with low confidence score"""
        is_valid, errors = self.validator.validate_extraction(
            vendor_id="VEND001",
            iban="IE29AIBK93115212345678",
            account_name="Test Account",
            confidence_score=0.50  # Below threshold
        )
        
        assert is_valid is False
        assert any("Confidence score" in error for error in errors)
    
    def test_empty_account_name(self):
        """Test validation with empty account name"""
        is_valid, errors = self.validator.validate_extraction(
            vendor_id="VEND001",
            iban="IE29AIBK93115212345678",
            account_name="",
            confidence_score=0.95
        )
        
        assert is_valid is False
        assert any("Account name" in error for error in errors)
    
    def test_validate_account_name_valid(self):
        """Test account name validation with valid name"""
        assert self.validator.validate_account_name("Test Account") is True
    
    def test_validate_account_name_too_short(self):
        """Test account name validation with too short name"""
        assert self.validator.validate_account_name("A") is False
    
    def test_validate_account_name_empty(self):
        """Test account name validation with empty name"""
        assert self.validator.validate_account_name("") is False
    
    def test_confidence_level_high(self):
        """Test confidence level categorization - high"""
        level = self.validator.get_confidence_level(0.95)
        assert level == 'high'
    
    def test_confidence_level_medium(self):
        """Test confidence level categorization - medium"""
        level = self.validator.get_confidence_level(0.80)
        assert level == 'medium'
    
    def test_confidence_level_low(self):
        """Test confidence level categorization - low"""
        level = self.validator.get_confidence_level(0.50)
        assert level == 'low'
    
    def test_validate_batch_consistency(self):
        """Test batch validation"""
        extractions = [
            {
                'vendor_id': 'VEND001',
                'iban': 'IE29AIBK93115212345678',
                'account_name': 'Test Account 1',
                'confidence_score': 0.95
            },
            {
                'vendor_id': 'VEND002',
                'iban': 'INVALID',
                'account_name': 'Test Account 2',
                'confidence_score': 0.80
            }
        ]
        
        result = self.validator.validate_batch_consistency(extractions)
        
        assert len(result['valid']) == 1
        assert len(result['invalid']) == 1
