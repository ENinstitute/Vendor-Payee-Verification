"""
Invoice Processor
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

from typing import Dict, Optional
from pathlib import Path
import time

from src.ai_processor.anthropic_client import AnthropicClient
from src.ai_processor.pattern_recognizer import PatternRecognizer
from src.validators.iban_validator import iban_validator
from src.validators.data_validator import data_validator
from src.utils.logger import get_logger
from src.utils.security import security_manager
from config.settings import settings

logger = get_logger(__name__)


class InvoiceProcessor:
    """Processes individual invoices for IBAN extraction"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.ai_client = AnthropicClient()
        self.pattern_recognizer = PatternRecognizer(db_manager)
    
    def process_invoice(self, invoice_path: str, vendor_id: str, 
                       learn_pattern: bool = False) -> Dict:
        """
        Process a single invoice to extract IBAN and account name
        
        Args:
            invoice_path: Path to invoice file
            vendor_id: Vendor identifier
            learn_pattern: Whether to learn and store the pattern
        
        Returns:
            Dictionary with extraction results
        """
        start_time = time.time()
        
        logger.info(f"Processing invoice: {invoice_path} for vendor {vendor_id}")
        
        try:
            # Validate file
            if not security_manager.validate_file_size(invoice_path):
                raise ValueError("File size exceeds limit")
            
            filename = Path(invoice_path).name
            if not security_manager.validate_file_type(filename):
                raise ValueError("Unsupported file type")
            
            # Get existing pattern if available
            existing_pattern = self.pattern_recognizer.get_pattern(vendor_id)
            
            # If learning mode or no pattern exists, analyze pattern
            if learn_pattern or not existing_pattern:
                logger.info("Analyzing invoice pattern...")
                pattern_data = self.ai_client.analyze_invoice_pattern(invoice_path)
                
                if learn_pattern:
                    # Store the pattern
                    pattern_id = self.pattern_recognizer.store_pattern(
                        vendor_id=vendor_id,
                        pattern_data=pattern_data,
                        confidence_score=pattern_data.get('confidence', 0.0)
                    )
                    
                    # Save to file for backup
                    self.pattern_recognizer.save_pattern_to_file(vendor_id, pattern_data)
                
                extraction_pattern = pattern_data
            else:
                extraction_pattern = existing_pattern
            
            # Extract IBAN and account name
            logger.info("Extracting IBAN and account name...")
            extraction_result = self.ai_client.extract_iban_and_account(
                invoice_path,
                pattern=extraction_pattern
            )
            
            # Validate IBAN
            iban = extraction_result.get('iban', '')
            is_valid_iban, formatted_iban, iban_error = iban_validator.validate(iban)
            
            if is_valid_iban:
                extraction_result['iban'] = formatted_iban
                extraction_result['iban_valid'] = True
            else:
                extraction_result['iban_valid'] = False
                extraction_result['iban_error'] = iban_error
                logger.warning(f"IBAN validation failed: {iban_error}")
            
            # Validate complete extraction
            is_valid, errors = data_validator.validate_extraction(
                vendor_id=vendor_id,
                iban=extraction_result.get('iban', ''),
                account_name=extraction_result.get('account_name', ''),
                confidence_score=extraction_result.get('confidence', 0.0)
            )
            
            extraction_result['validation_status'] = 'valid' if is_valid else 'invalid'
            extraction_result['validation_errors'] = errors
            
            # Store extraction in database
            pattern_id = existing_pattern.get('pattern_id') if existing_pattern else None
            
            extraction_id = self.db_manager.insert_extraction(
                vendor_id=vendor_id,
                pattern_id=pattern_id,
                invoice_filename=filename,
                iban=extraction_result.get('iban', ''),
                account_name=extraction_result.get('account_name', ''),
                confidence_score=extraction_result.get('confidence', 0.0)
            )
            
            extraction_result['extraction_id'] = extraction_id
            extraction_result['vendor_id'] = vendor_id
            extraction_result['invoice_filename'] = filename
            
            # Calculate processing time
            processing_time = time.time() - start_time
            extraction_result['processing_time'] = processing_time
            
            logger.info(f"Invoice processed successfully in {processing_time:.2f}s")
            logger.info(f"IBAN: {security_manager.mask_iban(extraction_result.get('iban', ''))} "
                       f"(Confidence: {extraction_result.get('confidence', 0.0):.2f})")
            
            return extraction_result
            
        except Exception as e:
            logger.error(f"Error processing invoice: {str(e)}")
            return {
                'vendor_id': vendor_id,
                'invoice_filename': Path(invoice_path).name if invoice_path else 'unknown',
                'iban': None,
                'account_name': None,
                'confidence': 0.0,
                'validation_status': 'error',
                'validation_errors': [str(e)],
                'processing_time': time.time() - start_time
            }
    
    def process_training_invoice(self, invoice_path: str, vendor_id: str) -> Dict:
        """
        Process an invoice in training mode (learns pattern)
        
        Args:
            invoice_path: Path to invoice file
            vendor_id: Vendor identifier
        
        Returns:
            Dictionary with extraction results
        """
        logger.info(f"Processing training invoice for vendor {vendor_id}")
        return self.process_invoice(invoice_path, vendor_id, learn_pattern=True)
