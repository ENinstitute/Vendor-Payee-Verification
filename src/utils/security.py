"""
Security Utilities
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import hashlib
import re
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64

from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SecurityManager:
    """Manages encryption and security operations"""
    
    def __init__(self):
        self.encryption_key = settings.ENCRYPTION_KEY
        self.fernet = None
        
        if self.encryption_key:
            self.fernet = Fernet(self.encryption_key.encode())
    
    def encrypt_data(self, data: str) -> Optional[str]:
        """
        Encrypt sensitive data
        
        Args:
            data: String to encrypt
        
        Returns:
            Encrypted string or None if encryption fails
        """
        if not self.fernet:
            logger.warning("Encryption key not configured")
            return data
        
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            return None
    
    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """
        Decrypt sensitive data
        
        Args:
            encrypted_data: Encrypted string
        
        Returns:
            Decrypted string or None if decryption fails
        """
        if not self.fernet:
            logger.warning("Encryption key not configured")
            return encrypted_data
        
        try:
            decrypted = self.fernet.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            return None
    
    @staticmethod
    def hash_pattern(pattern_data: str) -> str:
        """
        Generate hash for invoice pattern
        
        Args:
            pattern_data: String representation of pattern
        
        Returns:
            SHA-256 hash of pattern
        """
        return hashlib.sha256(pattern_data.encode()).hexdigest()
    
    @staticmethod
    def mask_iban(iban: str, show_last: int = 4) -> str:
        """
        Mask IBAN for logging/display purposes
        
        Args:
            iban: Full IBAN
            show_last: Number of characters to show at the end
        
        Returns:
            Masked IBAN (e.g., IE**************1234)
        """
        if not iban or len(iban) <= show_last:
            return iban
        
        # Keep country code and last N characters
        country_code = iban[:2] if len(iban) >= 2 else ""
        masked_middle = "*" * (len(iban) - show_last - 2)
        visible_end = iban[-show_last:]
        
        return f"{country_code}{masked_middle}{visible_end}"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal
        
        Args:
            filename: Original filename
        
        Returns:
            Sanitized filename
        """
        # Remove path separators and special characters
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        
        # Prevent hidden files
        if sanitized.startswith('.'):
            sanitized = '_' + sanitized[1:]
        
        return sanitized
    
    @staticmethod
    def validate_file_size(file_path: str) -> bool:
        """
        Validate file size is within limits
        
        Args:
            file_path: Path to file
        
        Returns:
            True if file size is acceptable
        """
        import os
        
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            if file_size_mb > settings.MAX_FILE_SIZE_MB:
                logger.warning(f"File exceeds size limit: {file_size_mb:.2f}MB > {settings.MAX_FILE_SIZE_MB}MB")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error checking file size: {str(e)}")
            return False
    
    @staticmethod
    def validate_file_type(filename: str) -> bool:
        """
        Validate file type is supported
        
        Args:
            filename: Filename to check
        
        Returns:
            True if file type is supported
        """
        extension = filename.lower().split('.')[-1]
        
        if extension not in settings.SUPPORTED_FORMATS:
            logger.warning(f"Unsupported file type: {extension}")
            return False
        
        return True
    
    @staticmethod
    def generate_encryption_key() -> str:
        """
        Generate a new Fernet encryption key
        
        Returns:
            Base64-encoded encryption key
        """
        return Fernet.generate_key().decode()


# Global security manager instance
security_manager = SecurityManager()
