"""
Anthropic Claude API Client
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import base64
from typing import Dict, Optional, List
from pathlib import Path
import anthropic

from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AnthropicClient:
    """Client for Anthropic Claude API"""
    
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.model = settings.ANTHROPIC_MODEL
        self.max_tokens = settings.ANTHROPIC_MAX_TOKENS
        self.temperature = settings.ANTHROPIC_TEMPERATURE
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        logger.info(f"Anthropic client initialized with model: {self.model}")
    
    def analyze_invoice_pattern(self, document_path: str) -> Dict:
        """
        Analyze invoice layout pattern using Claude
        
        Args:
            document_path: Path to invoice document
        
        Returns:
            Dictionary with pattern analysis
        """
        logger.info(f"Analyzing invoice pattern: {document_path}")
        
        try:
            # Read document
            file_extension = Path(document_path).suffix.lower()
            
            # Prepare document for Claude
            if file_extension == '.pdf':
                document_data = self._read_pdf(document_path)
            else:
                document_data = self._read_image(document_path)
            
            # Create prompt for pattern recognition
            prompt = self._create_pattern_recognition_prompt()
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": document_data['media_type'],
                                    "data": document_data['data']
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse response
            pattern_data = self._parse_pattern_response(response_text)
            
            logger.info("Pattern analysis completed successfully")
            return pattern_data
            
        except Exception as e:
            logger.error(f"Error analyzing invoice pattern: {str(e)}")
            raise
    
    def extract_iban_and_account(self, document_path: str, pattern: Optional[Dict] = None) -> Dict:
        """
        Extract IBAN and account name from invoice
        
        Args:
            document_path: Path to invoice document
            pattern: Optional pre-identified pattern to guide extraction
        
        Returns:
            Dictionary with extracted data
        """
        logger.info(f"Extracting IBAN and account from: {document_path}")
        
        try:
            # Read document
            file_extension = Path(document_path).suffix.lower()
            
            if file_extension == '.pdf':
                document_data = self._read_pdf(document_path)
            else:
                document_data = self._read_image(document_path)
            
            # Create extraction prompt
            prompt = self._create_extraction_prompt(pattern)
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": document_data['media_type'],
                                    "data": document_data['data']
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse extraction result
            extraction_data = self._parse_extraction_response(response_text)
            
            logger.info(f"Extraction completed: IBAN found={bool(extraction_data.get('iban'))}")
            return extraction_data
            
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            raise
    
    def _read_pdf(self, pdf_path: str) -> Dict:
        """Read PDF file and convert to base64"""
        from pdf2image import convert_from_path
        from io import BytesIO
        
        # Convert first page to image
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        
        if not images:
            raise ValueError("Could not convert PDF to image")
        
        # Convert image to base64
        buffer = BytesIO()
        images[0].save(buffer, format='PNG')
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            'media_type': 'image/png',
            'data': image_data
        }
    
    def _read_image(self, image_path: str) -> Dict:
        """Read image file and convert to base64"""
        from PIL import Image
        from io import BytesIO
        
        # Open and convert image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')
        
        # Determine format
        file_extension = Path(image_path).suffix.lower()
        format_map = {
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.png': 'PNG',
            '.tiff': 'PNG',  # Convert TIFF to PNG
            '.tif': 'PNG'
        }
        
        image_format = format_map.get(file_extension, 'PNG')
        
        # Convert to base64
        buffer = BytesIO()
        image.save(buffer, format=image_format)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        media_type = f"image/{image_format.lower()}"
        
        return {
            'media_type': media_type,
            'data': image_data
        }
    
    def _create_pattern_recognition_prompt(self) -> str:
        """Create prompt for pattern recognition"""
        return """Analyze this invoice document and identify the layout pattern for IBAN and bank account information.

Please provide the following information in JSON format:

{
  "layout_type": "standard|complex|custom",
  "iban_section": {
    "location": "header|footer|middle|sidebar",
    "label": "the label/heading text near the IBAN",
    "context": "description of surrounding elements"
  },
  "account_section": {
    "location": "header|footer|middle|sidebar",
    "label": "the label/heading text near the account name",
    "context": "description of surrounding elements"
  },
  "confidence": 0.0-1.0,
  "notes": "any additional observations"
}

Focus on the structural layout and location patterns, not the actual data values."""
    
    def _create_extraction_prompt(self, pattern: Optional[Dict]) -> str:
        """Create prompt for data extraction"""
        base_prompt = """Extract the IBAN and bank account name/identifier from this invoice document.

Please provide the following information in JSON format:

{
  "iban": "the full IBAN number",
  "account_name": "the bank account name or identifier",
  "confidence": 0.0-1.0,
  "notes": "any extraction notes or uncertainties"
}

Rules:
- Extract the complete IBAN including country code and check digits
- Remove any spaces or formatting from the IBAN
- Extract the account name exactly as shown
- Set confidence to 1.0 only if you are absolutely certain
- Use confidence 0.7-0.9 if there is any uncertainty
- Include notes if the data is unclear or ambiguous"""
        
        if pattern:
            base_prompt += f"\n\nContext: Previous analysis indicated IBAN is typically located in {pattern.get('iban_location', 'unknown')} section."
        
        return base_prompt
    
    def _parse_pattern_response(self, response: str) -> Dict:
        """Parse Claude's pattern recognition response"""
        import json
        
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in pattern response")
                return {
                    'layout_type': 'unknown',
                    'confidence': 0.5,
                    'raw_response': response
                }
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing pattern JSON: {str(e)}")
            return {
                'layout_type': 'unknown',
                'confidence': 0.5,
                'raw_response': response
            }
    
    def _parse_extraction_response(self, response: str) -> Dict:
        """Parse Claude's extraction response"""
        import json
        
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                
                # Clean IBAN (remove spaces)
                if data.get('iban'):
                    data['iban'] = data['iban'].replace(' ', '').upper()
                
                return data
            else:
                logger.warning("No JSON found in extraction response")
                return {
                    'iban': None,
                    'account_name': None,
                    'confidence': 0.0,
                    'notes': 'Failed to parse response',
                    'raw_response': response
                }
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing extraction JSON: {str(e)}")
            return {
                'iban': None,
                'account_name': None,
                'confidence': 0.0,
                'notes': f'JSON parse error: {str(e)}',
                'raw_response': response
            }
