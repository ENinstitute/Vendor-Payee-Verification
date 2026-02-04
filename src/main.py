"""
Main Entry Point
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
from src.processors.batch_processor import BatchProcessor
from src.utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


def train_model():
    """Train the AI model with sample invoices"""
    logger.info("=== IBAN Extraction System - Training Mode ===")
    logger.info(f"Training directory: {settings.INVOICES_TRAINING_DIR}")
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Initialize batch processor
    batch_processor = BatchProcessor(db_manager)
    
    # TODO: Load vendor mapping from configuration file
    # For now, use a simple mapping based on filename prefixes
    vendor_mapping = {
        # Example: "vendor1_invoice.pdf": "VEND001"
        # This should be loaded from a config file in production
    }
    
    # Process training batch
    results = batch_processor.process_training_batch(
        str(settings.INVOICES_TRAINING_DIR),
        vendor_mapping
    )
    
    logger.info("Training completed!")
    logger.info(f"Results: {results['successful']}/{results['total']} successful")
    logger.info(f"Average confidence: {results['average_confidence']:.2f}")


def process_invoices():
    """Process invoices using trained model"""
    logger.info("=== IBAN Extraction System - Processing Mode ===")
    logger.info(f"Processing directory: {settings.INVOICES_PROCESSING_DIR}")
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Initialize batch processor
    batch_processor = BatchProcessor(db_manager)
    
    # TODO: Load vendor mapping from configuration file
    vendor_mapping = {}
    
    # Process production batch
    results = batch_processor.process_production_batch(
        str(settings.INVOICES_PROCESSING_DIR),
        vendor_mapping
    )
    
    logger.info("Processing completed!")
    logger.info(f"Results: {results['successful']}/{results['total']} successful")
    logger.info(f"CSV output: {results.get('csv_output', 'N/A')}")
    logger.info(f"Validation report: {results.get('validation_report', 'N/A')}")


def load_to_dynamics():
    """Load extracted data to Dynamics GP"""
    logger.info("=== IBAN Extraction System - Dynamics GP Loading ===")
    
    # TODO: Implement Dynamics GP loading logic
    logger.warning("Dynamics GP loading not yet implemented")
    logger.info("Please manually load CSV file to Dynamics GP using SQL scripts")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py train      - Train model with sample invoices")
        print("  python main.py process    - Process invoices")
        print("  python main.py load       - Load data to Dynamics GP")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "train":
        train_model()
    elif command == "process":
        process_invoices()
    elif command == "load":
        load_to_dynamics()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
