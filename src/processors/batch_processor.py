"""
Batch Processor
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

from typing import List, Dict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from src.processors.invoice_processor import InvoiceProcessor
from src.output.csv_generator import CSVGenerator
from src.utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


class BatchProcessor:
    """Processes multiple invoices in batch"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.invoice_processor = InvoiceProcessor(db_manager)
        self.csv_generator = CSVGenerator()
        self.max_workers = settings.MAX_WORKERS
    
    def process_training_batch(self, invoice_directory: str, vendor_mapping: Dict[str, str]) -> Dict:
        """
        Process training batch of invoices (learns patterns)
        
        Args:
            invoice_directory: Directory containing training invoices
            vendor_mapping: Dict mapping filename patterns to vendor IDs
        
        Returns:
            Dictionary with batch results
        """
        logger.info(f"Processing training batch from: {invoice_directory}")
        
        # Get all invoice files
        invoice_files = self._get_invoice_files(invoice_directory)
        
        if not invoice_files:
            logger.warning("No invoice files found in directory")
            return {'success': False, 'message': 'No files found'}
        
        results = []
        
        logger.info(f"Processing {len(invoice_files)} training invoices...")
        
        # Process sequentially for training (to learn patterns properly)
        for invoice_path in tqdm(invoice_files, desc="Training"):
            vendor_id = self._get_vendor_id(invoice_path, vendor_mapping)
            
            if not vendor_id:
                logger.warning(f"Could not determine vendor for: {invoice_path.name}")
                continue
            
            result = self.invoice_processor.process_training_invoice(
                str(invoice_path),
                vendor_id
            )
            results.append(result)
        
        # Generate summary
        summary = self._generate_summary(results)
        summary['mode'] = 'training'
        
        logger.info(f"Training batch completed: {summary['successful']}/{summary['total']} successful")
        
        return summary
    
    def process_production_batch(self, invoice_directory: str, vendor_mapping: Dict[str, str]) -> Dict:
        """
        Process production batch of invoices (uses learned patterns)
        
        Args:
            invoice_directory: Directory containing invoices to process
            vendor_mapping: Dict mapping filename patterns to vendor IDs
        
        Returns:
            Dictionary with batch results
        """
        logger.info(f"Processing production batch from: {invoice_directory}")
        
        # Get all invoice files
        invoice_files = self._get_invoice_files(invoice_directory)
        
        if not invoice_files:
            logger.warning("No invoice files found in directory")
            return {'success': False, 'message': 'No files found'}
        
        results = []
        
        logger.info(f"Processing {len(invoice_files)} invoices with {self.max_workers} workers...")
        
        # Process in parallel for efficiency
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_invoice = {}
            for invoice_path in invoice_files:
                vendor_id = self._get_vendor_id(invoice_path, vendor_mapping)
                
                if not vendor_id:
                    logger.warning(f"Could not determine vendor for: {invoice_path.name}")
                    continue
                
                future = executor.submit(
                    self.invoice_processor.process_invoice,
                    str(invoice_path),
                    vendor_id,
                    False  # Don't learn patterns in production
                )
                future_to_invoice[future] = invoice_path
            
            # Collect results with progress bar
            for future in tqdm(as_completed(future_to_invoice), total=len(future_to_invoice), desc="Processing"):
                invoice_path = future_to_invoice[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error processing {invoice_path.name}: {str(e)}")
                    results.append({
                        'invoice_filename': invoice_path.name,
                        'validation_status': 'error',
                        'validation_errors': [str(e)]
                    })
        
        # Generate summary
        summary = self._generate_summary(results)
        summary['mode'] = 'production'
        
        # Generate CSV output
        valid_extractions = [r for r in results if r.get('validation_status') == 'valid']
        if valid_extractions:
            csv_path = self.csv_generator.generate_csv(valid_extractions)
            summary['csv_output'] = csv_path
        
        # Generate validation report
        report_path = self.csv_generator.generate_validation_report(results)
        summary['validation_report'] = report_path
        
        logger.info(f"Production batch completed: {summary['successful']}/{summary['total']} successful")
        
        return summary
    
    def _get_invoice_files(self, directory: str) -> List[Path]:
        """Get all invoice files from directory"""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"Directory not found: {directory}")
            return []
        
        invoice_files = []
        
        for format_ext in settings.SUPPORTED_FORMATS:
            invoice_files.extend(dir_path.glob(f"*.{format_ext}"))
        
        return sorted(invoice_files)
    
    def _get_vendor_id(self, invoice_path: Path, vendor_mapping: Dict[str, str]) -> str:
        """
        Determine vendor ID from filename
        
        Args:
            invoice_path: Path to invoice file
            vendor_mapping: Dict mapping patterns to vendor IDs
        
        Returns:
            Vendor ID or None
        """
        filename = invoice_path.name.lower()
        
        # Try exact match first
        if filename in vendor_mapping:
            return vendor_mapping[filename]
        
        # Try pattern matching
        for pattern, vendor_id in vendor_mapping.items():
            if pattern.lower() in filename:
                return vendor_id
        
        # Try extracting from filename (e.g., "VEND001_invoice.pdf" -> "VEND001")
        parts = invoice_path.stem.split('_')
        if parts:
            potential_id = parts[0]
            if potential_id.isalnum():
                return potential_id
        
        return None
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """Generate summary statistics from results"""
        total = len(results)
        successful = len([r for r in results if r.get('validation_status') == 'valid'])
        failed = len([r for r in results if r.get('validation_status') in ['invalid', 'error']])
        
        # Calculate average confidence for successful extractions
        valid_results = [r for r in results if r.get('validation_status') == 'valid']
        avg_confidence = sum(r.get('confidence', 0.0) for r in valid_results) / len(valid_results) if valid_results else 0.0
        
        # Calculate average processing time
        avg_time = sum(r.get('processing_time', 0.0) for r in results) / total if total > 0 else 0.0
        
        # Count by confidence level
        high_confidence = len([r for r in valid_results if r.get('confidence', 0.0) >= settings.MAX_CONFIDENCE_THRESHOLD])
        medium_confidence = len([r for r in valid_results if settings.MIN_CONFIDENCE_THRESHOLD <= r.get('confidence', 0.0) < settings.MAX_CONFIDENCE_THRESHOLD])
        low_confidence = len([r for r in valid_results if r.get('confidence', 0.0) < settings.MIN_CONFIDENCE_THRESHOLD])
        
        summary = {
            'success': True,
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0.0,
            'average_confidence': avg_confidence,
            'average_processing_time': avg_time,
            'confidence_distribution': {
                'high': high_confidence,
                'medium': medium_confidence,
                'low': low_confidence
            },
            'results': results
        }
        
        return summary
