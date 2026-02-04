# AI-Powered IBAN Extraction System

**Chartered Accountants Ireland**  
**Version 1.0.0**

An AI-powered system to automatically extract IBAN and bank account information from vendor invoices using Anthropic Claude API, designed for Dynamics GP integration.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Security & Compliance](#security--compliance)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## 🎯 Overview

This system processes approximately 800 vendor invoices to extract:
- **IBAN** (International Bank Account Number)
- **Bank Account Names/Identifiers**

### Key Statistics
- **Target Accuracy**: >95%
- **Processing Time**: <30 seconds per invoice
- **Training Set**: 100 invoices
- **Production Set**: ~700 invoices
- **Confidence Threshold**: >90%

---

## ✨ Features

### Core Capabilities
- ✅ **AI-Powered Extraction** using Anthropic Claude API
- ✅ **Pattern Recognition** for invoice layouts
- ✅ **IBAN Validation** with checksum verification
- ✅ **Batch Processing** with parallel execution
- ✅ **CSV Export** for Dynamics GP integration
- ✅ **Comprehensive Logging** and audit trails
- ✅ **Security Controls** with encryption support
- ✅ **Alert System** for suspicious changes

### Supported Formats
- PDF documents
- Image files (JPG, JPEG, PNG, TIFF)

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  Invoice Files  │
│  (PDF/Images)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Anthropic Claude API   │
│  - Pattern Recognition   │
│  - Data Extraction       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│    Validation Layer      │
│  - IBAN Validator        │
│  - Data Validator        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│    Database Layer        │
│  - PostgreSQL/SQLite     │
│  - Pattern Storage       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│     CSV Output           │
│  - Dynamics GP Import    │
│  - Validation Reports    │
└─────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 12+ (or SQLite for development)
- Anthropic API Key
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/ENinstitute/Vendor-Payee-Verification.git
cd Vendor-Payee-Verification
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your configuration
notepad .env
```

### Step 5: Initialize Database
```bash
python src/main.py init-db
```

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file with your settings:

```ini
# Anthropic API
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Database
DB_TYPE=postgresql  # or sqlite for development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iban_extraction
DB_USER=your_user
DB_PASSWORD=your_password

# Application
ENV=development
LOG_LEVEL=INFO
MAX_CONFIDENCE_THRESHOLD=0.90
MIN_CONFIDENCE_THRESHOLD=0.70

# Security
ENCRYPTION_KEY=your_32_char_encryption_key

# Processing
MAX_WORKERS=4
BATCH_SIZE=50
```

---

## 🚀 Usage

### Training Mode
Train the AI model with 100 sample invoices:

```bash
# Place training invoices in data/invoices/training/
python scripts/train_model.py
```

### Processing Mode
Process production invoices:

```bash
# Place invoices in data/invoices/processing/
python scripts/process_invoices.py
```

### Alternative: Direct Command
```bash
python src/main.py train      # Training mode
python src/main.py process    # Processing mode
python src/main.py load       # Load to Dynamics GP
```

### Output Files
- **CSV Output**: `data/output/iban_extractions_YYYYMMDD_HHMMSS.csv`
- **Validation Report**: `data/output/validation_report_YYYYMMDD_HHMMSS.csv`
- **Logs**: `logs/iban_extraction_YYYYMMDD.log`

---

## 📁 Project Structure

```
iban-extraction-system/
├── config/                    # Configuration module
│   ├── __init__.py
│   └── settings.py           # Settings management
├── database/                  # Database layer
│   ├── __init__.py
│   ├── db_manager.py         # Database operations
│   ├── schema.sql            # Database schema
│   └── migrations/           # Schema migrations
├── src/                       # Source code
│   ├── __init__.py
│   ├── main.py               # Main entry point
│   ├── ai_processor/         # AI processing
│   │   ├── anthropic_client.py
│   │   └── pattern_recognizer.py
│   ├── extractors/           # Data extractors (future)
│   ├── validators/           # Validation logic
│   │   ├── iban_validator.py
│   │   └── data_validator.py
│   ├── processors/           # Processing logic
│   │   ├── invoice_processor.py
│   │   └── batch_processor.py
│   ├── output/               # Output generation
│   │   └── csv_generator.py
│   └── utils/                # Utilities
│       ├── logger.py
│       └── security.py
├── tests/                     # Test suite
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── data/                      # Data directories
│   ├── invoices/
│   │   ├── training/        # Training invoices
│   │   └── processing/      # Production invoices
│   ├── patterns/            # Stored patterns
│   └── output/              # Generated outputs
├── docs/                      # Documentation
│   ├── architecture.md
│   ├── api_documentation.md
│   ├── deployment.md
│   └── compliance/
│       ├── DPIA_template.md
│       └── LIA_template.md
├── scripts/                   # Execution scripts
│   ├── train_model.py
│   ├── process_invoices.py
│   └── load_to_dynamics.py
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
└── README.md                 # This file
```

---

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/unit/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test
```bash
pytest tests/unit/test_iban_validator.py -v
```

---

## 🔒 Security & Compliance

### GDPR Compliance
- Data Privacy Impact Assessment (DPIA) required
- Legitimate Interest Assessment (LIA) required
- Templates available in `docs/compliance/`

### Security Features
- ✅ Encryption at rest and in transit
- ✅ Access control (5 levels)
- ✅ Audit logging
- ✅ Alert system for suspicious patterns
- ✅ IBAN masking in logs
- ✅ File validation (size, type)

### Access Levels
1. **Level 1** - Hostinger Server: Eduardo, Sylvan (backup)
2. **Level 2** - Git Repository: Eduardo, Alan, Deniz, Kieran
3. **Level 3** - Database: Kieran, Altamash, Eduardo
4. **Level 4** - Azure Storage: Kieran, Altamash
5. **Level 5** - Dynamics GP: Altamash, Kieran

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Anthropic API Error
```
Error: Invalid API key
Solution: Check ANTHROPIC_API_KEY in .env file
```

#### 2. Database Connection Failed
```
Error: Could not connect to database
Solution: Verify DB credentials and PostgreSQL is running
```

#### 3. Low Confidence Scores
```
Issue: Extractions below 70% confidence
Solution: Retrain with more diverse invoice samples
```

#### 4. File Not Supported
```
Error: Unsupported file type
Solution: Ensure file is PDF, JPG, JPEG, PNG, or TIFF
```

### Logs Location
Check logs in `logs/iban_extraction_YYYYMMDD.log` for detailed error information.

---

## 📞 Support

### Project Team

| Name | Role | Email |
|------|------|-------|
| Kieran Daly | Data Architect | kieran.daly@charteredaccountants.ie |
| Eduardo Nascimento | Solutions Architect | eduardo.nascimento@charteredaccountants.ie |
| Altamash Naik | ERP Architect | altamash.naik@charteredaccountants.ie |

### Documentation
- **Architecture**: `docs/architecture.md`
- **API Docs**: `docs/api_documentation.md`
- **Deployment**: `docs/deployment.md`

### Reporting Issues
Use GitHub Issues or contact the project team directly.

---

## 📄 License

Copyright © 2025 Chartered Accountants Ireland  
All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 🎯 Project Goals

- [x] Extract IBANs with >95% accuracy
- [x] Process ~800 invoices
- [x] Generate CSV for Dynamics GP
- [x] GDPR compliance documentation
- [x] Comprehensive testing
- [x] Security controls implementation

---

**Built with ❤️ by Chartered Accountants Ireland IT Team**
