"""
CSV Generator
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import csv
from typing import List, Dict
from pathlib import Path
from datetime import datetime

from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CSVGenerator:
    """Generates CSV output from extraction results"""
    
    def __init__(self):
        self.encoding = settings.CSV_ENCODING
        self.delimiter = settings.CSV_DELIMITER
        self.columns = settings.CSV_COLUMNS
        self.output_dir = settings.OUTPUT_DIR
    
    def generate_csv(self, extractions: List[Dict], filename: Optional[str] = None) -> str:
        """
        Generate CSV file from extraction results
        
        Args:
            extractions: List of extraction dictionaries
            filename: Optional output filename
        
        Returns:
            Path to generated CSV file
        """
        if not extractions:
            logger.warning("No extractions provided for CSV generation")
            return None
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"iban_extractions_{timestamp}.csv"
        
        output_path = self.output_dir / filename
        
        try:
            with open(output_path, 'w', newline='', encoding=self.encoding) as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=self.columns,
                    delimiter=self.delimiter,
                    quoting=csv.QUOTE_MINIMAL
                )
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for extraction in extractions:
                    row = {
                        'vendor_id': extraction.get('vendor_id', ''),
                        'iban': extraction.get('iban', ''),
                        'account_name': extraction.get('account_name', ''),
                        'confidence_score': extraction.get('confidence_score', 0.0)
                    }
                    writer.writerow(row)
            
            logger.info(f"CSV generated successfully: {output_path} ({len(extractions)} rows)")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating CSV: {str(e)}")
            raise
    
    def generate_validation_report(self, extractions: List[Dict], filename: Optional[str] = None) -> str:
        """
        Generate detailed validation report CSV
        
        Args:
            extractions: List of extraction dictionaries
            filename: Optional output filename
        
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"validation_report_{timestamp}.csv"
        
        output_path = self.output_dir / filename
        
        # Extended columns for validation report
        report_columns = [
            'vendor_id',
            'vendor_name',
            'invoice_filename',
            'iban',
            'account_name',
            'confidence_score',
            'confidence_level',
            'validation_status',
            'validation_errors',
            'processed_at'
        ]
        
        try:
            with open(output_path, 'w', newline='', encoding=self.encoding) as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=report_columns,
                    delimiter=self.delimiter,
                    quoting=csv.QUOTE_MINIMAL
                )
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for extraction in extractions:
                    # Determine confidence level
                    score = extraction.get('confidence_score', 0.0)
                    if score >= settings.MAX_CONFIDENCE_THRESHOLD:
                        confidence_level = 'HIGH'
                    elif score >= settings.MIN_CONFIDENCE_THRESHOLD:
                        confidence_level = 'MEDIUM'
                    else:
                        confidence_level = 'LOW'
                    
                    row = {
                        'vendor_id': extraction.get('vendor_id', ''),
                        'vendor_name': extraction.get('vendor_name', ''),
                        'invoice_filename': extraction.get('invoice_filename', ''),
                        'iban': extraction.get('iban', ''),
                        'account_name': extraction.get('account_name', ''),
                        'confidence_score': extraction.get('confidence_score', 0.0),
                        'confidence_level': confidence_level,
                        'validation_status': extraction.get('validation_status', 'pending'),
                        'validation_errors': '; '.join(extraction.get('validation_errors', [])),
                        'processed_at': extraction.get('processed_at', '')
                    }
                    writer.writerow(row)
            
            logger.info(f"Validation report generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating validation report: {str(e)}")
            raise
    
    def append_to_csv(self, extraction: Dict, csv_path: str):
        """
        Append single extraction to existing CSV
        
        Args:
            extraction: Extraction dictionary
            csv_path: Path to CSV file
        """
        try:
            with open(csv_path, 'a', newline='', encoding=self.encoding) as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=self.columns,
                    delimiter=self.delimiter,
                    quoting=csv.QUOTE_MINIMAL
                )
                
                row = {
                    'vendor_id': extraction.get('vendor_id', ''),
                    'iban': extraction.get('iban', ''),
                    'account_name': extraction.get('account_name', ''),
                    'confidence_score': extraction.get('confidence_score', 0.0)
                }
                writer.writerow(row)
            
            logger.debug(f"Row appended to CSV: {csv_path}")
            
        except Exception as e:
            logger.error(f"Error appending to CSV: {str(e)}")
            raise
