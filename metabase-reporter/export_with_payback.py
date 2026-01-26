"""
Sales Retention Analysis with Payback Calculations

Pulls cohort retention data from Metabase and creates comprehensive payback analysis
with acquisition costs from Google Sheets.

Output: Excel file with 6 sheets showing Pivot, Cumulative, and Payback analysis
for both "Net Losses Full" and "Net Losses + Affiliate Payouts" cohorts.
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import openpyxl
from openpyxl.styles import numbers

# Import configuration
import config

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIALS_FILE = r'C:\Users\Tom Young\OneDrive\Desktop\credentials.json'

# Metabase card IDs
CARD_12462 = 12462  # Net Losses Full
CARD_13018 = 13018  # Net Losses AND Affiliate Payouts

# Google Sheets IDs
ACTUALS_SHEET_ID = '1-kbUBDVdLIXf0bbG4C_c7JWbyipGQtCdWjW7R7agiaM'
BUDGET_SHEET_ID = '1PY4MPmPXptZ3p4kJOmtS-mP35AfMq2DAvFG56CA9ffQ'


def get_sheets_service():
    """Create Google Sheets API service"""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=credentials)


def fetch_actuals_spend():
    """Fetch actuals spend data from Google Sheets"""
    service = get_sheets_service()

    # Fetch actuals from Sheet1
    result = service.spreadsheets().values().get(
        spreadsheetId=ACTUALS_SHEET_ID,
        range='Sheet1!B2:F100'
    ).execute()

    values = result.get('values', [])

    spend_data = {}
    for row in values:
        if len(row) >= 4:  # Need at least Month, Total, Sales, Affiliate
            month_str = row[0]
            try:
                # Parse the month
                month_date = pd.to_datetime(month_str, errors='coerce')
                if pd.isna(month_date):
                    continue

                month_key = month_date.strftime('%Y-%m')

                # Helper to parse numbers with commas
                def parse_num(val):
                    if not val:
                        return 0
                    if isinstance(val, str):
                        return float(val.replace(',', ''))
                    return float(val)

                sales = parse_num(row[2]) if len(row) > 2 else 0
                affiliate = parse_num(row[3]) if len(row) > 3 else 0
                marketing = parse_num(row[4]) if len(row) > 4 else 0

                spend_data[month_key] = {
                    'sales': sales,
                    'affiliate': affiliate,
                    'marketing': marketing
                }
            except:
                continue

    return spend_data


def fetch_budget_for_current_month():
    """Fetch budget data for January 2026 from Budget Summary sheet"""
    service = get_sheets_service()

    # Fetch the specific cells
    ranges = ['G27', 'G34', 'G42', 'G53']
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=BUDGET_SHEET_ID,
        ranges=[f"'Budget Summary'!{r}" for r in ranges]
    ).execute()

    values = result.get('valueRanges', [])

    # Helper function to convert string with commas to float
    def parse_number(value):
        if isinstance(value, str):
            return float(value.replace(',', ''))
        return float(value)

    # Extract values
    creator_referral = parse_number(values[0].get('values', [[0]])[0][0]) if values[0].get('values') else 0
    sales_spend = parse_number(values[1].get('values', [[0]])[0][0]) if values[1].get('values') else 0
    am_spend = parse_number(values[2].get('values', [[0]])[0][0]) if values[2].get('values') else 0
    total_marketing = parse_number(values[3].get('values', [[0]])[0][0]) if values[3].get('values') else 0

    # Calculate final values
    sales = sales_spend + am_spend - creator_referral
    affiliate = creator_referral
    marketing = total_marketing

    return {
        '2026-01': {
            'sales': sales,
            'affiliate': affiliate,
            'marketing': marketing
        }
    }


def fetch_metabase_data(card_id):
    """Fetch data from Metabase card"""
    url = f"{config.METABASE_URL}/api/card/{card_id}/query/json"
    headers = {
        "X-API-KEY": config.METABASE_API_KEY
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()


def create_pivot_table(data):
    """Create pivot table with first_transaction_month as rows, period as columns"""
    df = pd.DataFrame(data)

    # Debug: Print available columns
    print(f"Available columns: {df.columns.tolist()}")
    print(f"First few rows:\n{df.head()}")

    # Parse dates
    df['first_transaction_month'] = pd.to_datetime(df['first_transaction_month'])

    # Create pivot
    pivot = df.pivot_table(
        index='first_transaction_month',
        columns='period',
        values='contribution_profit',
        aggfunc='sum'
    )

    # Sort by date
    pivot = pivot.sort_index()

    # Format index as YYYY-MM
    pivot.index = pivot.index.strftime('%Y-%m')

    return pivot


def create_cumulative_table(pivot):
    """Create cumulative table that only shows values for periods that have occurred"""
    cumulative = pd.DataFrame(index=pivot.index, columns=pivot.columns)

    current_date = datetime.now()

    for cohort in pivot.index:
        # Parse cohort date
        try:
            cohort_date = pd.to_datetime(cohort)
        except:
            continue

        # Calculate months elapsed since cohort
        months_elapsed = (current_date.year - cohort_date.year) * 12 + (current_date.month - cohort_date.month) + 1

        # Calculate cumulative values
        row_values = pivot.loc[cohort].values
        cumulative_values = []
        running_sum = 0

        for period_idx, val in enumerate(row_values):
            period_num = period_idx + 1

            if period_num <= months_elapsed:
                if not pd.isna(val):
                    running_sum += val
                cumulative_values.append(running_sum)
            else:
                cumulative_values.append(np.nan)

        cumulative.loc[cohort] = cumulative_values

    return cumulative


def create_payback_table(cumulative, spend_data, spend_type):
    """
    Create payback table with acquisition costs and payback ratios

    spend_type: 'net_losses_full' (Sales + Affiliate) or 'net_losses_affiliate' (Sales only)
    """
    payback = pd.DataFrame(index=cumulative.index)

    # Add acquisition cost column
    acq_costs = []
    for cohort_month in cumulative.index:
        if cohort_month in spend_data:
            if spend_type == 'net_losses_full':
                # Sales + Affiliate
                cost = spend_data[cohort_month]['sales'] + spend_data[cohort_month]['affiliate']
            else:
                # Sales only
                cost = spend_data[cohort_month]['sales']
            acq_costs.append(cost)
        else:
            acq_costs.append(0)

    payback['Acquisition Cost'] = acq_costs

    # Add payback ratios for each period
    for col in cumulative.columns:
        payback[f'Period {col}'] = cumulative[col] / payback['Acquisition Cost']

    return payback


def format_excel_sheet(writer, sheet_name, df, is_currency=True, is_percentage=False):
    """Format Excel sheet with proper number formatting"""
    df.to_excel(writer, sheet_name=sheet_name)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Get the dimensions
    max_row = len(df) + 1
    max_col = len(df.columns) + 1

    # Apply formatting
    for row in range(2, max_row + 1):
        for col in range(2, max_col + 1):
            cell = worksheet.cell(row=row, column=col)
            if is_percentage:
                cell.number_format = '0.00%'
            elif is_currency:
                cell.number_format = '$#,##0'

    return worksheet


def main():
    """Main execution function"""
    print("Fetching spend data from Google Sheets...")
    actuals_spend = fetch_actuals_spend()
    budget_spend = fetch_budget_for_current_month()

    # Combine actuals and budget
    all_spend = {**actuals_spend, **budget_spend}

    print(f"Loaded spend data for {len(all_spend)} months")

    # Create timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'Sales_Payback_Analysis_{timestamp}.xlsx'

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Process Card 12462 (Net Losses Full)
        print("\nProcessing Card 12462 (Net Losses Full)...")
        data_12462 = fetch_metabase_data(CARD_12462)
        pivot_12462 = create_pivot_table(data_12462)
        cumulative_12462 = create_cumulative_table(pivot_12462)
        payback_12462 = create_payback_table(cumulative_12462, all_spend, 'net_losses_full')

        format_excel_sheet(writer, 'Net Losses Full - Pivot', pivot_12462, is_currency=True)
        format_excel_sheet(writer, 'Net Losses Full - Cumulative', cumulative_12462, is_currency=True)
        format_excel_sheet(writer, 'Net Losses Full - Payback', payback_12462, is_currency=False, is_percentage=True)

        # Process Card 13018 (Net Losses + Affiliate Payouts)
        print("Processing Card 13018 (Net Losses + Affiliate Payouts)...")
        data_13018 = fetch_metabase_data(CARD_13018)
        pivot_13018 = create_pivot_table(data_13018)
        cumulative_13018 = create_cumulative_table(pivot_13018)
        payback_13018 = create_payback_table(cumulative_13018, all_spend, 'net_losses_affiliate')

        format_excel_sheet(writer, 'Net Losses+Affiliate - Pivot', pivot_13018, is_currency=True)
        format_excel_sheet(writer, 'Net Losses+Affiliate - Cumulative', cumulative_13018, is_currency=True)
        format_excel_sheet(writer, 'Net Losses+Affiliate - Payback', payback_13018, is_currency=False, is_percentage=True)

    print(f"\n✓ Analysis complete! Output saved to: {output_file}")


if __name__ == "__main__":
    main()
