-- AI-Powered IBAN Extraction System
-- Database Schema for PostgreSQL
-- Chartered Accountants Ireland
-- Version 1.0

-- ========================================
-- VENDORS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id VARCHAR(50) PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    is_priority BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vendors_priority ON vendors(is_priority);
CREATE INDEX idx_vendors_name ON vendors(vendor_name);

-- ========================================
-- INVOICE_PATTERNS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS invoice_patterns (
    pattern_id SERIAL PRIMARY KEY,
    vendor_id VARCHAR(50) REFERENCES vendors(vendor_id),
    pattern_hash VARCHAR(64) UNIQUE NOT NULL,
    layout_description TEXT,
    iban_location JSONB,  -- Stores coordinates/pattern for IBAN location
    account_name_location JSONB,  -- Stores coordinates/pattern for account name
    confidence_score DECIMAL(5,4) DEFAULT 0.0,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patterns_vendor ON invoice_patterns(vendor_id);
CREATE INDEX idx_patterns_hash ON invoice_patterns(pattern_hash);
CREATE INDEX idx_patterns_confidence ON invoice_patterns(confidence_score);

-- ========================================
-- EXTRACTIONS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS extractions (
    extraction_id SERIAL PRIMARY KEY,
    vendor_id VARCHAR(50) REFERENCES vendors(vendor_id),
    pattern_id INTEGER REFERENCES invoice_patterns(pattern_id),
    invoice_filename VARCHAR(255) NOT NULL,
    iban VARCHAR(34),  -- Max IBAN length is 34 characters
    account_name VARCHAR(255),
    confidence_score DECIMAL(5,4) DEFAULT 0.0,
    validation_status VARCHAR(20) DEFAULT 'pending',  -- pending, validated, rejected, corrected
    validation_notes TEXT,
    validated_by VARCHAR(100),
    validated_at TIMESTAMP,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_extractions_vendor ON extractions(vendor_id);
CREATE INDEX idx_extractions_pattern ON extractions(pattern_id);
CREATE INDEX idx_extractions_status ON extractions(validation_status);
CREATE INDEX idx_extractions_confidence ON extractions(confidence_score);
CREATE INDEX idx_extractions_iban ON extractions(iban);

-- ========================================
-- EXTRACTION_LOGS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS extraction_logs (
    log_id SERIAL PRIMARY KEY,
    extraction_id INTEGER REFERENCES extractions(extraction_id),
    log_level VARCHAR(20) NOT NULL,  -- DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_message TEXT NOT NULL,
    log_data JSONB,  -- Additional structured data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_extraction ON extraction_logs(extraction_id);
CREATE INDEX idx_logs_level ON extraction_logs(log_level);
CREATE INDEX idx_logs_created ON extraction_logs(created_at);

-- ========================================
-- ALERTS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL,  -- pattern_change, iban_change, low_confidence, etc.
    severity VARCHAR(20) NOT NULL,  -- low, medium, high, critical
    vendor_id VARCHAR(50) REFERENCES vendors(vendor_id),
    extraction_id INTEGER REFERENCES extractions(extraction_id),
    alert_message TEXT NOT NULL,
    alert_data JSONB,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_by VARCHAR(100),
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alerts_type ON alerts(alert_type);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_resolved ON alerts(resolved);
CREATE INDEX idx_alerts_vendor ON alerts(vendor_id);
CREATE INDEX idx_alerts_created ON alerts(created_at);

-- ========================================
-- PROCESSING_STATS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS processing_stats (
    stat_id SERIAL PRIMARY KEY,
    processing_date DATE NOT NULL,
    total_processed INTEGER DEFAULT 0,
    successful_extractions INTEGER DEFAULT 0,
    failed_extractions INTEGER DEFAULT 0,
    average_confidence DECIMAL(5,4) DEFAULT 0.0,
    average_processing_time DECIMAL(10,2) DEFAULT 0.0,  -- in seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stats_date ON processing_stats(processing_date);

-- ========================================
-- TRIGGERS FOR UPDATED_AT
-- ========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_vendors_updated_at BEFORE UPDATE ON vendors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patterns_updated_at BEFORE UPDATE ON invoice_patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_extractions_updated_at BEFORE UPDATE ON extractions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- VIEWS
-- ========================================

-- View for extraction summary by vendor
CREATE OR REPLACE VIEW v_vendor_extraction_summary AS
SELECT 
    v.vendor_id,
    v.vendor_name,
    v.is_priority,
    COUNT(e.extraction_id) as total_extractions,
    SUM(CASE WHEN e.validation_status = 'validated' THEN 1 ELSE 0 END) as validated_count,
    SUM(CASE WHEN e.validation_status = 'rejected' THEN 1 ELSE 0 END) as rejected_count,
    AVG(e.confidence_score) as avg_confidence,
    MAX(e.processed_at) as last_processed
FROM vendors v
LEFT JOIN extractions e ON v.vendor_id = e.vendor_id
GROUP BY v.vendor_id, v.vendor_name, v.is_priority;

-- View for active alerts
CREATE OR REPLACE VIEW v_active_alerts AS
SELECT 
    a.alert_id,
    a.alert_type,
    a.severity,
    a.vendor_id,
    v.vendor_name,
    a.alert_message,
    a.created_at,
    e.iban,
    e.confidence_score
FROM alerts a
LEFT JOIN vendors v ON a.vendor_id = v.vendor_id
LEFT JOIN extractions e ON a.extraction_id = e.extraction_id
WHERE a.resolved = FALSE
ORDER BY 
    CASE a.severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END,
    a.created_at DESC;

-- View for low confidence extractions
CREATE OR REPLACE VIEW v_low_confidence_extractions AS
SELECT 
    e.extraction_id,
    e.vendor_id,
    v.vendor_name,
    e.invoice_filename,
    e.iban,
    e.account_name,
    e.confidence_score,
    e.validation_status,
    e.processed_at
FROM extractions e
JOIN vendors v ON e.vendor_id = v.vendor_id
WHERE e.confidence_score < 0.90
ORDER BY e.confidence_score ASC, e.processed_at DESC;

-- ========================================
-- INITIAL DATA
-- ========================================

-- Insert default processing stats record
INSERT INTO processing_stats (processing_date, total_processed, successful_extractions, failed_extractions)
VALUES (CURRENT_DATE, 0, 0, 0)
ON CONFLICT DO NOTHING;

-- ========================================
-- COMMENTS
-- ========================================
COMMENT ON TABLE vendors IS 'Stores vendor information from Dynamics GP';
COMMENT ON TABLE invoice_patterns IS 'Stores learned invoice layout patterns for each vendor';
COMMENT ON TABLE extractions IS 'Stores extracted IBAN and account name data';
COMMENT ON TABLE extraction_logs IS 'Audit log for all extraction operations';
COMMENT ON TABLE alerts IS 'Stores system alerts for suspicious patterns or errors';
COMMENT ON TABLE processing_stats IS 'Daily processing statistics';
