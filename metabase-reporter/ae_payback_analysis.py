"""
Account Executive Payback Analysis

Pulls AE-level cohort retention data from Metabase and creates individual payback
analysis for each Account Executive, including wages, T&E, and bonus costs.

Output: Excel file with one tab per AE showing cumulative profit and payback analysis.
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

# Metabase card ID
CARD_13796 = 13796  # AE-level retention data

# Google Sheets ID for AE data
AE_SHEET_ID = '1-kbUBDVdLIXf0bbG4C_c7JWbyipGQtCdWjW7R7agiaM'


def get_sheets_service():
    """Create Google Sheets API service"""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=credentials)


def fetch_ae_costs():
    """Fetch AE cost data from Google Sheets"""
    service = get_sheets_service()

    result = service.spreadsheets().values().get(
        spreadsheetId=AE_SHEET_ID,
        range="'Account Executives'!B3:G100"
    ).execute()

    values = result.get('values', [])

    ae_costs = {}
    for row in values:
        if len(row) >= 6:
            ae_name = row[0].strip()
            try:
                monthly_wages = float(row[3]) if row[3] else 0
                monthly_te = float(row[4]) if row[4] else 0
                bonus_str = row[5] if row[5] else '0%'
                bonus_pct = float(bonus_str.strip('%')) / 100 if '%' in bonus_str else 0

                ae_costs[ae_name] = {
                    'monthly_wages': monthly_wages,
                    'monthly_te': monthly_te,
                    'bonus_pct': bonus_pct
                }
            except:
                continue

    return ae_costs


def fetch_metabase_data(card_id):
    """Fetch data from Metabase card"""
    url = f"{config.METABASE_URL}/api/card/{card_id}/query/json"
    headers = {
        "X-API-KEY": config.METABASE_API_KEY
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()


def create_pivot_table(data, ae_name):
    """Create pivot table for specific AE"""
    df = pd.DataFrame(data)

    # Filter for this AE
    df = df[df['account_executive'] == ae_name].copy()

    if df.empty:
        return None

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
    if pivot is None:
        return None

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


def create_payback_table(cumulative, ae_cost_data):
    """
    Create payback table with AE costs and payback ratios

    Acquisition Cost = Monthly Wages + Monthly T&E + (Bonus % × Latest Cumulative Profit)
    """
    if cumulative is None:
        return None

    payback = pd.DataFrame(index=cumulative.index)

    monthly_wages = ae_cost_data['monthly_wages']
    monthly_te = ae_cost_data['monthly_te']
    bonus_pct = ae_cost_data['bonus_pct']

    # Calculate latest cumulative for each cohort (for bonus calculation)
    latest_cumulative = cumulative.apply(
        lambda row: row.dropna().iloc[-1] if len(row.dropna()) > 0 else 0,
        axis=1
    )

    # Calculate bonus costs
    bonus_costs = latest_cumulative * bonus_pct

    # Calculate total acquisition cost
    base_cost = monthly_wages + monthly_te
    total_costs = base_cost + bonus_costs

    # Add cost columns
    payback['Monthly Wages'] = monthly_wages
    payback['Monthly T&E'] = monthly_te
    payback['Bonus Cost'] = bonus_costs
    payback['Total Acq Cost'] = total_costs

    # Add payback ratios for each period
    for col in cumulative.columns:
        payback[f'Period {col}'] = cumulative[col] / total_costs

    return payback


def write_ae_sheet(writer, ae_name, cumulative, payback):
    """Write AE data to a single sheet with cumulative on top and payback below"""
    # Create valid sheet name (Excel has 31 char limit and doesn't allow special chars)
    sheet_name = ae_name[:31].replace('/', '-').replace('\\', '-').replace('*', '-')

    # Write cumulative table first
    cumulative.to_excel(writer, sheet_name=sheet_name, startrow=0)

    # Write payback table below with spacing
    start_row = cumulative.shape[0] + 3
    payback.to_excel(writer, sheet_name=sheet_name, startrow=start_row)

    # Get worksheet for formatting
    worksheet = writer.sheets[sheet_name]

    # Format cumulative section (currency)
    for row in range(2, cumulative.shape[0] + 2):
        for col in range(2, cumulative.shape[1] + 2):
            cell = worksheet.cell(row=row, column=col)
            cell.number_format = '$#,##0'

    # Format payback section
    payback_start_row = start_row + 1
    for row in range(payback_start_row + 1, payback_start_row + payback.shape[0] + 1):
        # First 4 columns are costs (currency)
        for col in range(2, 6):
            cell = worksheet.cell(row=row, column=col)
            cell.number_format = '$#,##0'

        # Remaining columns are percentages
        for col in range(6, payback.shape[1] + 2):
            cell = worksheet.cell(row=row, column=col)
            cell.number_format = '0.00%'

    # Add section header for payback
    header_cell = worksheet.cell(row=start_row, column=1)
    header_cell.value = "Payback Analysis"
    header_cell.font = openpyxl.styles.Font(bold=True)


def main():
    """Main execution function"""
    print("Fetching AE cost data from Google Sheets...")
    ae_costs = fetch_ae_costs()
    print(f"Loaded cost data for {len(ae_costs)} AEs")

    print("\nFetching AE retention data from Metabase...")
    data = fetch_metabase_data(CARD_13796)
    print(f"Loaded {len(data)} rows of retention data")

    # Create timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'AE_Payback_Analysis_{timestamp}.xlsx'

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        ae_count = 0

        # Process each AE
        for ae_name, cost_data in ae_costs.items():
            print(f"\nProcessing {ae_name}...")

            # Create tables
            pivot = create_pivot_table(data, ae_name)

            if pivot is None or pivot.empty:
                print(f"  ⚠ No data found for {ae_name}, skipping...")
                continue

            cumulative = create_cumulative_table(pivot)
            payback = create_payback_table(cumulative, cost_data)

            # Write to Excel
            write_ae_sheet(writer, ae_name, cumulative, payback)

            ae_count += 1
            print(f"  ✓ Added tab for {ae_name}")

    print(f"\n✓ Analysis complete! Processed {ae_count} AEs")
    print(f"✓ Output saved to: {output_file}")


if __name__ == "__main__":
    main()
