# Metabase GTM Analysis Tools

Automated sales and account executive payback analysis from Metabase data.

## Overview

This toolkit provides two main analysis scripts:

1. **Sales Retention Analysis** - Overall sales cohort payback with spend tracking
2. **AE Payback Analysis** - Individual account executive performance and payback curves

## Features

- 📊 Pulls cohort retention data from Metabase
- 💰 Calculates cumulative LTV and payback ratios
- 📈 Tracks acquisition costs (Sales + Affiliate + Marketing spend)
- 👥 Individual AE performance analysis with wages, T&E, and bonus tracking
- 📅 Automatically handles actuals vs budget data
- 📑 Generates formatted Excel reports with multiple views

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Settings

Copy `config_example.py` to `config.py` and fill in your credentials:

```bash
cp config_example.py config.py
```

Edit `config.py` with:
- Metabase API key
- Google Sheets credentials path (if using)
- Other configuration options

### 3. Set Up Google Sheets Access

Place your `credentials.json` file (from Google Cloud Console) in the project directory or specify the path in your scripts.

**Required Google Sheets:**
- Actuals spend sheet (Sales, Affiliate, Marketing by month)
- Budget Summary sheet (for current month projections)
- Account Executives sheet (wages, T&E, bonus structure)

## Usage

### Sales Retention Analysis

Generates overall sales cohort payback analysis:

```bash
python export_with_payback.py
```

**Output:** Excel file with 6 sheets
- Net Losses Full: Pivot, Cumulative, Payback (Sales + Affiliate spend)
- Net Losses + Affiliate Payouts: Pivot, Cumulative, Payback (Sales only)

**Data Sources:**
- Metabase cards: 12462, 13018
- Actuals from spend tracking sheet
- Budget from Budget Summary tab for incomplete months

### AE Payback Analysis

Generates individual account executive performance analysis:

```bash
python ae_payback_analysis.py
```

**Output:** Excel file with one tab per AE containing:
- Cumulative profit by cohort
- Payback analysis with cost breakdown (Wages + T&E + Bonus)

**Data Sources:**
- Metabase card: 13796 (AE-level retention data)
- Account Executives sheet for cost data

## File Structure

```
metabase-reporter/
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── config_example.py             # Configuration template
├── config.py                     # Your config (not in git)
├── export_with_payback.py        # Sales retention analysis
├── ae_payback_analysis.py        # AE payback analysis
├── .gitignore                    # Protects sensitive files
└── credentials.json              # Google creds (not in git)
```

## Configuration

### Metabase Cards

The scripts reference specific Metabase question IDs:
- **12462**: Sales gross profit retention adjusted for net losses (full)
- **13018**: Sales gross profit retention adjusted for net losses AND affiliate payouts
- **13796**: Account Executive gross profit retention (AE breakdown)

### Google Sheets Structure

**Actuals Spend Sheet:**
- Column B: Month
- Column D: Sales spend
- Column E: Affiliate spend
- Column F: Marketing spend

**Budget Summary Sheet:**
- Cell G27: Creator referral (Affiliate)
- Cell G34: Sales Spend
- Cell G42: AM Spend
- Cell G53: Total Marketing

**Account Executives Sheet:**
- Column B: AE Name
- Column E: Monthly Wages
- Column F: Monthly T&E
- Column G: Bonus % (e.g., "10%")

## Cost Calculations

### Sales-Level Costs
- **Net Losses Full**: Sales spend + Affiliate spend
- **Net Losses + Affiliate Payouts**: Sales spend only (affiliate already deducted from cohorts)

### AE-Level Costs
For each cohort month:
```
Total Acq Cost = Monthly Wages + Monthly T&E + Bonus Cost
Bonus Cost = Bonus % × Latest Cumulative Profit
```

## Output Format

### Sales Reports
- **Pivot**: Original contribution profit by cohort × period
- **Cumulative**: Running total profit (only for periods that occurred)
- **Payback**: Acquisition costs + payback ratio (cumulative profit / cost)

### AE Reports
Each AE tab shows:
1. **Cumulative Table** (top): Cumulative profit by cohort and period
2. **Payback Table** (bottom): Monthly Wages | Monthly T&E | Bonus Cost | Total Acq Cost | Payback % by period

## Tips

- Output files are timestamped so you never overwrite previous reports
- Only active AEs (from Google Sheet) are included in AE analysis
- Payback ratios shown as percentages (e.g., 35% = not yet paid back, 150% = 1.5x return)
- Budget data used for incomplete months, actuals for completed months

## Troubleshooting

**No data found:**
- Verify Metabase API key is correct
- Check that card IDs haven't changed
- Ensure you have network access to Metabase

**Google Sheets errors:**
- Confirm credentials.json is in the correct location
- Verify sheets are shared with the service account email
- Check sheet names and cell references match exactly

**Missing AEs:**
- Only AEs listed in the Account Executives Google Sheet are processed
- Verify AE names match exactly between Metabase and Google Sheets

## Security

- ✅ `config.py` and `credentials.json` are excluded from Git
- ✅ Never commit API keys or passwords
- ✅ Output files (*.xlsx, *.csv) are excluded from Git
- ⚠️ Keep your credentials secure

## Requirements

- Python 3.7+
- Google Sheets API access
- Metabase API key
- Required Python packages (see requirements.txt)

## License

Internal use only
