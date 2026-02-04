# Quick Start Guide

## AI-Powered IBAN Extraction System

This guide will help you get started with the IBAN Extraction System in under 10 minutes.

---

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Anthropic API Key (get from https://console.anthropic.com/)
- [ ] PostgreSQL installed (or use SQLite for testing)
- [ ] Git installed

---

## 5-Minute Setup

### 1. Get the Code
```bash
git clone https://github.com/ENinstitute/Vendor-Payee-Verification.git
cd Vendor-Payee-Verification
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
copy .env.example .env
notepad .env  # Edit with your settings
```

**Minimum Required Settings:**
```ini
ANTHROPIC_API_KEY=your_key_here
DB_TYPE=sqlite  # Use SQLite for quick start
```

### 5. Test Installation
```bash
python -c "from src.validators.iban_validator import iban_validator; print('Setup successful!')"
```

---

## First Run - Training Mode

### Step 1: Prepare Training Data
Place 100 sample invoices in:
```
data/invoices/training/
```

**Naming Convention:**
- `VEND001_invoice1.pdf`
- `VEND002_invoice1.pdf`
- etc.

### Step 2: Run Training
```bash
python scripts/train_model.py
```

**Expected Output:**
```
INFO: Processing training batch from: data/invoices/training
Training: 100%|████████████| 100/100
INFO: Training completed!
INFO: Results: 95/100 successful
INFO: Average confidence: 0.93
```

---

## Second Run - Processing Mode

### Step 1: Add Production Invoices
Place invoices in:
```
data/invoices/processing/
```

### Step 2: Run Processing
```bash
python scripts/process_invoices.py
```

### Step 3: Check Output
Look for:
- `data/output/iban_extractions_YYYYMMDD_HHMMSS.csv`
- `data/output/validation_report_YYYYMMDD_HHMMSS.csv`

---

## Verify Results

### Check CSV Output
```bash
# View first 10 lines
head -n 10 data/output/iban_extractions_*.csv
```

**Expected Format:**
```csv
vendor_id,iban,account_name,confidence_score
VEND001,IE29AIBK93115212345678,Vendor Name,0.95
VEND002,GB82WEST12345698765432,Another Vendor,0.92
```

### Check Logs
```bash
# View latest log
type logs\iban_extraction_*.log
```

---

## Common First-Time Issues

### Issue 1: API Key Error
```
Error: ANTHROPIC_API_KEY not configured
```
**Fix:** Add your API key to `.env` file

### Issue 2: No Invoices Found
```
Warning: No invoice files found in directory
```
**Fix:** Ensure PDF/image files are in correct directory

### Issue 3: Import Error
```
ModuleNotFoundError: No module named 'anthropic'
```
**Fix:** Run `pip install -r requirements.txt` again

---

## Next Steps

1. **Review Results**: Check validation report for low confidence extractions
2. **Manual Review**: Verify IBANs for high-priority vendors
3. **Load to Dynamics GP**: Use generated CSV
4. **Read Full Documentation**: See `README.md` for advanced features

---

## Quick Commands Reference

```bash
# Training
python scripts/train_model.py

# Processing
python scripts/process_invoices.py

# Run tests
pytest tests/unit/ -v

# Check logs
type logs\iban_extraction_*.log
```

---

## Getting Help

- **Documentation**: `README.md`
- **Issues**: GitHub Issues
- **Email**: eduardo.nascimento@charteredaccountants.ie

---

**Ready to process 800 invoices? Let's go! 🚀**
