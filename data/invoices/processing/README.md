# Processing Invoice Directory

Place your ~700 production invoices here for batch processing.

## File Naming Convention

Use vendor ID prefixes in filenames:
- `VEND001_202501_invoice.pdf`
- `VEND002_202501_invoice.pdf`
- etc.

## Supported Formats
- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- TIFF (`.tiff`, `.tif`)

## Processing

Once files are in place, run:
```bash
python scripts/process_invoices.py
```

The system will:
1. Use learned patterns from training
2. Extract IBAN and account names
3. Validate all extractions
4. Generate CSV output
5. Create validation report

## Output Location

Results will be saved to:
- `../../output/iban_extractions_YYYYMMDD_HHMMSS.csv`
- `../../output/validation_report_YYYYMMDD_HHMMSS.csv`
