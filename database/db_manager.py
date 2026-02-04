"""
Database Manager
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import psycopg2
import sqlite3
from typing import Optional, Dict, List, Any, Tuple
from contextlib import contextmanager
from pathlib import Path
import json

from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.db_type = settings.DB_TYPE
        self.connection = None
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(settings.SQLITE_DB_PATH)
                conn.row_factory = sqlite3.Row
            else:  # postgresql
                conn = psycopg2.connect(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    database=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD
                )
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def initialize_database(self):
        """Initialize database with schema"""
        logger.info("Initializing database...")
        
        # Read schema file
        schema_path = Path(__file__).parent / "schema.sql"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                # SQLite doesn't support all PostgreSQL features, adapt schema
                schema_sql = self._adapt_schema_for_sqlite(schema_sql)
            
            # Split and execute statements
            statements = schema_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        logger.warning(f"Statement execution warning: {str(e)}")
            
            cursor.close()
        
        logger.info("Database initialized successfully")
    
    def _adapt_schema_for_sqlite(self, schema: str) -> str:
        """Adapt PostgreSQL schema for SQLite"""
        # Replace SERIAL with INTEGER PRIMARY KEY AUTOINCREMENT
        schema = schema.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        
        # Remove JSONB (use TEXT instead)
        schema = schema.replace("JSONB", "TEXT")
        
        # Remove specific PostgreSQL features
        schema = schema.replace("DECIMAL(5,4)", "REAL")
        schema = schema.replace("DECIMAL(10,2)", "REAL")
        
        return schema
    
    # Vendor Operations
    def insert_vendor(self, vendor_id: str, vendor_name: str, is_priority: bool = False) -> bool:
        """Insert a new vendor"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO vendors (vendor_id, vendor_name, is_priority)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (vendor_id) DO UPDATE SET
                        vendor_name = EXCLUDED.vendor_name,
                        is_priority = EXCLUDED.is_priority,
                        updated_at = CURRENT_TIMESTAMP
                    """ if self.db_type == "postgresql" else
                    """
                    INSERT OR REPLACE INTO vendors (vendor_id, vendor_name, is_priority)
                    VALUES (?, ?, ?)
                    """,
                    (vendor_id, vendor_name, is_priority)
                )
                cursor.close()
            logger.info(f"Vendor {vendor_id} inserted/updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error inserting vendor: {str(e)}")
            return False
    
    def get_vendor(self, vendor_id: str) -> Optional[Dict[str, Any]]:
        """Get vendor by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM vendors WHERE vendor_id = %s" if self.db_type == "postgresql" else
                    "SELECT * FROM vendors WHERE vendor_id = ?",
                    (vendor_id,)
                )
                row = cursor.fetchone()
                cursor.close()
                
                if row:
                    if self.db_type == "sqlite":
                        return dict(row)
                    else:
                        columns = [desc[0] for desc in cursor.description]
                        return dict(zip(columns, row))
                return None
        except Exception as e:
            logger.error(f"Error getting vendor: {str(e)}")
            return None
    
    # Pattern Operations
    def insert_pattern(self, vendor_id: str, pattern_hash: str, layout_description: str,
                      iban_location: Dict, account_name_location: Dict, confidence_score: float) -> Optional[int]:
        """Insert a new invoice pattern"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Convert dicts to JSON strings for SQLite
                iban_loc_json = json.dumps(iban_location)
                account_loc_json = json.dumps(account_name_location)
                
                cursor.execute(
                    """
                    INSERT INTO invoice_patterns 
                    (vendor_id, pattern_hash, layout_description, iban_location, account_name_location, confidence_score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING pattern_id
                    """ if self.db_type == "postgresql" else
                    """
                    INSERT INTO invoice_patterns 
                    (vendor_id, pattern_hash, layout_description, iban_location, account_name_location, confidence_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (vendor_id, pattern_hash, layout_description, iban_loc_json, account_loc_json, confidence_score)
                )
                
                if self.db_type == "postgresql":
                    pattern_id = cursor.fetchone()[0]
                else:
                    pattern_id = cursor.lastrowid
                
                cursor.close()
                logger.info(f"Pattern {pattern_id} inserted for vendor {vendor_id}")
                return pattern_id
        except Exception as e:
            logger.error(f"Error inserting pattern: {str(e)}")
            return None
    
    def get_vendor_patterns(self, vendor_id: str) -> List[Dict[str, Any]]:
        """Get all patterns for a vendor"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM invoice_patterns 
                    WHERE vendor_id = %s 
                    ORDER BY usage_count DESC, confidence_score DESC
                    """ if self.db_type == "postgresql" else
                    """
                    SELECT * FROM invoice_patterns 
                    WHERE vendor_id = ? 
                    ORDER BY usage_count DESC, confidence_score DESC
                    """,
                    (vendor_id,)
                )
                rows = cursor.fetchall()
                cursor.close()
                
                patterns = []
                if self.db_type == "sqlite":
                    for row in rows:
                        pattern = dict(row)
                        # Parse JSON fields
                        if pattern.get('iban_location'):
                            pattern['iban_location'] = json.loads(pattern['iban_location'])
                        if pattern.get('account_name_location'):
                            pattern['account_name_location'] = json.loads(pattern['account_name_location'])
                        patterns.append(pattern)
                else:
                    columns = [desc[0] for desc in cursor.description]
                    patterns = [dict(zip(columns, row)) for row in rows]
                
                return patterns
        except Exception as e:
            logger.error(f"Error getting patterns: {str(e)}")
            return []
    
    # Extraction Operations
    def insert_extraction(self, vendor_id: str, pattern_id: Optional[int], invoice_filename: str,
                         iban: str, account_name: str, confidence_score: float) -> Optional[int]:
        """Insert extraction result"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO extractions 
                    (vendor_id, pattern_id, invoice_filename, iban, account_name, confidence_score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING extraction_id
                    """ if self.db_type == "postgresql" else
                    """
                    INSERT INTO extractions 
                    (vendor_id, pattern_id, invoice_filename, iban, account_name, confidence_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (vendor_id, pattern_id, invoice_filename, iban, account_name, confidence_score)
                )
                
                if self.db_type == "postgresql":
                    extraction_id = cursor.fetchone()[0]
                else:
                    extraction_id = cursor.lastrowid
                
                cursor.close()
                logger.info(f"Extraction {extraction_id} inserted for {invoice_filename}")
                return extraction_id
        except Exception as e:
            logger.error(f"Error inserting extraction: {str(e)}")
            return None
    
    def get_all_extractions(self, validated_only: bool = False) -> List[Dict[str, Any]]:
        """Get all extractions"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT e.*, v.vendor_name 
                    FROM extractions e
                    JOIN vendors v ON e.vendor_id = v.vendor_id
                """
                
                if validated_only:
                    query += " WHERE e.validation_status = 'validated'"
                
                query += " ORDER BY e.processed_at DESC"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                
                if self.db_type == "sqlite":
                    return [dict(row) for row in rows]
                else:
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error getting extractions: {str(e)}")
            return []
    
    # Alert Operations
    def insert_alert(self, alert_type: str, severity: str, vendor_id: str,
                    extraction_id: Optional[int], alert_message: str, alert_data: Optional[Dict] = None) -> Optional[int]:
        """Insert a new alert"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                alert_data_json = json.dumps(alert_data) if alert_data else None
                
                cursor.execute(
                    """
                    INSERT INTO alerts 
                    (alert_type, severity, vendor_id, extraction_id, alert_message, alert_data)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING alert_id
                    """ if self.db_type == "postgresql" else
                    """
                    INSERT INTO alerts 
                    (alert_type, severity, vendor_id, extraction_id, alert_message, alert_data)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (alert_type, severity, vendor_id, extraction_id, alert_message, alert_data_json)
                )
                
                if self.db_type == "postgresql":
                    alert_id = cursor.fetchone()[0]
                else:
                    alert_id = cursor.lastrowid
                
                cursor.close()
                logger.warning(f"Alert {alert_id} created: {alert_message}")
                return alert_id
        except Exception as e:
            logger.error(f"Error inserting alert: {str(e)}")
            return None
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active (unresolved) alerts"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM v_active_alerts")
                rows = cursor.fetchall()
                cursor.close()
                
                if self.db_type == "sqlite":
                    return [dict(row) for row in rows]
                else:
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error getting active alerts: {str(e)}")
            return []
