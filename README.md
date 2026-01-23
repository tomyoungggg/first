# Google Sheets Financial Analyzer

A Python script that connects to Google Sheets, pulls financial data, and performs comprehensive analysis.

## Features

- 🔐 Secure Google Sheets API integration using service account authentication
- 📊 Automatic data retrieval from your specified spreadsheet
- 💰 Financial data analysis with statistics and insights
- 📈 Category-based breakdowns and summaries
- 💾 CSV export functionality
- 📝 Detailed reporting with visualizations

## Quick Start

### 1. Set Up Google Sheets API Access

Follow the detailed instructions in [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) to:
- Create a Google Cloud project
- Enable Google Sheets API
- Create service account credentials
- Share your spreadsheet with the service account

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials

1. Download your `credentials.json` file from Google Cloud Console (see setup guide)
2. Place it in the project directory
3. The script is pre-configured to analyze: `2026 Budget [a.o. 12-25]`

### 4. Run the Analyzer

```bash
python financial_analyzer.py
```

## Configuration

You can customize the analyzer by editing the constants in `financial_analyzer.py`:

```python
CREDENTIALS_FILE = 'credentials.json'  # Path to your credentials
SPREADSHEET_NAME = '2026 Budget [a.o. 12-25]'  # Your spreadsheet name
SHEET_RANGE = 'A:Z'  # Range to fetch (e.g., 'Sheet1!A1:D100')
```

## Output

The script provides:

1. **Console Report**: Detailed analysis printed to the terminal
   - Dataset overview
   - Statistical summaries (total, average, median, etc.)
   - Category breakdowns
   - Key insights

2. **CSV Export**: `financial_data_export.csv` with the raw data

## Example Output

```
🚀 Starting Financial Analysis...
------------------------------------------------------------
✓ Successfully authenticated with Google Sheets API
✓ Found spreadsheet: 2026 Budget [a.o. 12-25]
✓ Retrieved 50 rows and 5 columns

============================================================
FINANCIAL ANALYSIS REPORT
============================================================
Report Generated: 2026-01-23 10:30:00
Data Source: 2026 Budget [a.o. 12-25]
============================================================

📊 Dataset Overview:
   Rows: 50
   Columns: 5

💰 Analyzing Numeric Columns:
   Found 2 numeric columns:
   - Amount
   - Budget

📈 Statistical Summary:
   Amount:
      Total: $15,234.56
      Average: $304.69
      Median: $250.00
      ...

💡 Key Insights:
   1. Total Amount: $15,234.56
   2. Average monthly spending: $1,269.55
   ...

✅ Analysis complete!
```

## Project Structure

```
.
├── README.md                    # This file
├── GOOGLE_SHEETS_SETUP.md       # Detailed setup instructions
├── financial_analyzer.py        # Main script
├── requirements.txt             # Python dependencies
├── credentials.json.example     # Example credentials structure
├── .gitignore                   # Git ignore file (protects credentials)
└── credentials.json            # Your credentials (DO NOT COMMIT)
```

## Security

- ✅ `credentials.json` is automatically excluded from Git
- ✅ Service accounts provide secure, limited access
- ✅ Read-only access to spreadsheets
- ⚠️ Never commit or share your `credentials.json` file

## Troubleshooting

See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for common issues and solutions.

## Requirements

- Python 3.7 or higher
- Google Cloud account
- Google Sheets spreadsheet with financial data

## License

This project is open source and available for personal and commercial use
