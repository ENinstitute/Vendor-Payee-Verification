"""
Pattern Recognizer
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

from typing import Dict, Optional, List
import json
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.security import security_manager
from config.settings import settings

logger = get_logger(__name__)


class PatternRecognizer:
    """Recognizes and stores invoice layout patterns"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.patterns_cache = {}
    
    def store_pattern(self, vendor_id: str, pattern_data: Dict, confidence_score: float) -> Optional[int]:
        """
        Store a recognized invoice pattern
        
        Args:
            vendor_id: Vendor identifier
            pattern_data: Pattern information from AI
            confidence_score: Confidence score of pattern recognition
        
        Returns:
            Pattern ID or None if storage failed
        """
        try:
            # Generate pattern hash
            pattern_string = json.dumps(pattern_data, sort_keys=True)
            pattern_hash = security_manager.hash_pattern(pattern_string)
            
            # Check if pattern already exists
            existing_patterns = self.db_manager.get_vendor_patterns(vendor_id)
            
            for existing in existing_patterns:
                if existing['pattern_hash'] == pattern_hash:
                    logger.info(f"Pattern already exists for vendor {vendor_id}")
                    return existing['pattern_id']
            
            # Create layout description
            layout_description = self._generate_layout_description(pattern_data)
            
            # Extract location information
            iban_location = pattern_data.get('iban_section', {})
            account_name_location = pattern_data.get('account_section', {})
            
            # Store pattern
            pattern_id = self.db_manager.insert_pattern(
                vendor_id=vendor_id,
                pattern_hash=pattern_hash,
                layout_description=layout_description,
                iban_location=iban_location,
                account_name_location=account_name_location,
                confidence_score=confidence_score
            )
            
            if pattern_id:
                # Cache pattern
                self.patterns_cache[vendor_id] = pattern_data
                logger.info(f"Pattern {pattern_id} stored for vendor {vendor_id}")
            
            return pattern_id
            
        except Exception as e:
            logger.error(f"Error storing pattern: {str(e)}")
            return None
    
    def get_pattern(self, vendor_id: str) -> Optional[Dict]:
        """
        Get the best pattern for a vendor
        
        Args:
            vendor_id: Vendor identifier
        
        Returns:
            Pattern dictionary or None
        """
        # Check cache first
        if vendor_id in self.patterns_cache:
            logger.debug(f"Pattern retrieved from cache for vendor {vendor_id}")
            return self.patterns_cache[vendor_id]
        
        # Get from database
        patterns = self.db_manager.get_vendor_patterns(vendor_id)
        
        if not patterns:
            logger.info(f"No patterns found for vendor {vendor_id}")
            return None
        
        # Return pattern with highest usage and confidence
        best_pattern = patterns[0]
        
        # Reconstruct pattern dict
        pattern_dict = {
            'pattern_id': best_pattern['pattern_id'],
            'layout_type': best_pattern.get('layout_description', ''),
            'iban_location': best_pattern.get('iban_location', {}),
            'account_name_location': best_pattern.get('account_name_location', {}),
            'confidence': best_pattern.get('confidence_score', 0.0)
        }
        
        # Cache it
        self.patterns_cache[vendor_id] = pattern_dict
        
        logger.info(f"Pattern {best_pattern['pattern_id']} retrieved for vendor {vendor_id}")
        return pattern_dict
    
    def find_similar_pattern(self, pattern_data: Dict, threshold: float = None) -> Optional[Dict]:
        """
        Find similar pattern across all vendors
        
        Args:
            pattern_data: Pattern to match
            threshold: Similarity threshold (default from settings)
        
        Returns:
            Similar pattern or None
        """
        if threshold is None:
            threshold = settings.PATTERN_SIMILARITY_THRESHOLD
        
        # This is a simplified implementation
        # In production, you might use more sophisticated similarity metrics
        
        pattern_hash = security_manager.hash_pattern(json.dumps(pattern_data, sort_keys=True))
        
        # Search in cache
        for vendor_id, cached_pattern in self.patterns_cache.items():
            cached_hash = security_manager.hash_pattern(json.dumps(cached_pattern, sort_keys=True))
            if cached_hash == pattern_hash:
                logger.info(f"Similar pattern found in cache for vendor {vendor_id}")
                return cached_pattern
        
        return None
    
    def _generate_layout_description(self, pattern_data: Dict) -> str:
        """Generate human-readable layout description"""
        layout_type = pattern_data.get('layout_type', 'unknown')
        
        iban_section = pattern_data.get('iban_section', {})
        iban_location = iban_section.get('location', 'unknown')
        
        account_section = pattern_data.get('account_section', {})
        account_location = account_section.get('location', 'unknown')
        
        description = f"Layout: {layout_type}, IBAN in {iban_location}, Account in {account_location}"
        
        return description
    
    def save_pattern_to_file(self, vendor_id: str, pattern_data: Dict):
        """
        Save pattern to JSON file for backup/analysis
        
        Args:
            vendor_id: Vendor identifier
            pattern_data: Pattern information
        """
        try:
            pattern_file = settings.PATTERNS_DIR / f"{vendor_id}_pattern.json"
            
            with open(pattern_file, 'w', encoding='utf-8') as f:
                json.dump(pattern_data, f, indent=2)
            
            logger.debug(f"Pattern saved to file: {pattern_file}")
            
        except Exception as e:
            logger.error(f"Error saving pattern to file: {str(e)}")
    
    def load_pattern_from_file(self, vendor_id: str) -> Optional[Dict]:
        """
        Load pattern from JSON file
        
        Args:
            vendor_id: Vendor identifier
        
        Returns:
            Pattern dictionary or None
        """
        try:
            pattern_file = settings.PATTERNS_DIR / f"{vendor_id}_pattern.json"
            
            if not pattern_file.exists():
                return None
            
            with open(pattern_file, 'r', encoding='utf-8') as f:
                pattern_data = json.load(f)
            
            logger.debug(f"Pattern loaded from file: {pattern_file}")
            return pattern_data
            
        except Exception as e:
            logger.error(f"Error loading pattern from file: {str(e)}")
            return None
