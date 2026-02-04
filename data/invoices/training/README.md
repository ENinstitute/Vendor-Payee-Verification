# Training Invoice Directory

Place your 100 training invoices here for the AI model to learn from.

## File Naming Convention

Use vendor ID prefixes in filenames:
- `VEND001_invoice1.pdf`
- `VEND001_invoice2.pdf`
- `VEND002_invoice1.pdf`
- etc.

## Supported Formats
- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- TIFF (`.tiff`, `.tif`)

## Best Practices

1. **Diverse Samples**: Include invoices with different layouts
2. **High Quality**: Ensure PDFs/images are clear and readable
3. **Representative**: Choose invoices that represent typical vendor patterns
4. **Size Limit**: Keep files under 10MB each

## Training Process

Once files are in place, run:
```bash
python scripts/train_model.py
```

The system will:
1. Analyze invoice layouts
2. Learn IBAN/account name positions
3. Store patterns in database
4. Generate confidence metrics
