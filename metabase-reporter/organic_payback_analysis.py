import pandas as pd
from datetime import datetime
import requests
from config import METABASE_URL, METABASE_API_KEY
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import numpy as np

print("=" * 80)
print("ORGANIC RETENTION ANALYSIS - COMPREHENSIVE REPORT")
print("=" * 80)

ACTUALS_SHEET_ID = '1-kbUBDVdLIXf0bbG4C_c7JWbyipGQtCdWjW7R7agiaM'
BUDGET_SUMMARY_SHEET_ID = '1PY4MPmPXptZ3p4kJOmtS-mP35AfMq2DAvFG56CA9ffQ'
CREDENTIALS_FILE = r'C:\Users\Tom Young\OneDrive\Desktop\credentials.json'

# Metabase card IDs
PROFIT_CARD_ID = 13830      # Organic gross profit retention (adjusted)
NET_LOSSES_CARD_ID = 13828  # Organic net losses
GTV_CARD_ID = 13831         # Organic GTV retention
LOGO_CARD_ID = 13829        # Organic logo retention

metabase_headers = {
    "X-API-KEY": METABASE_API_KEY,
    "Content-Type": "application/json"
}

# Step 1: Fetch ACTUALS Marketing spend (completed months)
print("\n1. Fetching ACTUALS Marketing spend (completed months)...")

try:
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=credentials)

    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=ACTUALS_SHEET_ID,
        range='Sheet1!B2:F100'
    ).execute()

    values = result.get('values', [])

    organic_spend = {}

    for row in values:
        if len(row) < 5:
            continue

        month_str = row[0]
        marketing_str = row[4]  # Column F is Marketing spend

        if not month_str or not marketing_str:
            continue

        try:
            month_date = pd.to_datetime(month_str, errors='coerce')
            if pd.isna(month_date):
                continue

            month_key = month_date.strftime('%Y-%m')
            marketing_val = float(str(marketing_str).replace('$', '').replace(',', '').strip())
            organic_spend[month_key] = marketing_val

        except:
            continue

    print(f"   ✓ Retrieved actuals for {len(organic_spend)} months")

except Exception as e:
    print(f"   ❌ Error: {e}")
    organic_spend = {}

# Step 2: Fetch BUDGET for current incomplete month (Jan 2026) from Marketing column
print("\n2. Fetching BUDGET spend for current month from Sheet1 Marketing column...")

try:
    # Re-read Sheet1 to get Jan 2026 from column F (Marketing)
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=ACTUALS_SHEET_ID,
        range='Sheet1!B2:F100'
    ).execute()

    values = result.get('values', [])

    for row in values:
        if len(row) < 5:
            continue

        month_str = row[0]

        if not month_str:
            continue

        try:
            month_date = pd.to_datetime(month_str, errors='coerce')
            if pd.isna(month_date):
                continue

            month_key = month_date.strftime('%Y-%m')

            # For Jan 2026, use Marketing column (F)
            if month_key == '2026-01' and len(row) >= 5 and row[4]:
                marketing_val = float(str(row[4]).replace('$', '').replace(',', '').strip())
                organic_spend['2026-01'] = marketing_val
                print(f"   ✓ Jan 2026 Budget (Marketing): ${marketing_val:,.0f}")
                break

        except:
            continue

except Exception as e:
    print(f"   ❌ Error: {e}")

print(f"\n   ✓ Total months with spend data: {len(organic_spend)}")


def fetch_and_process_card(card_id, card_name):
    """Fetch data from Metabase and create pivot"""
    print(f"\n3. Fetching {card_name} (Card {card_id})...")

    try:
        response = requests.post(
            f"{METABASE_URL}/api/card/{card_id}/query/json",
            headers=metabase_headers
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            print(f"   ✓ Retrieved {len(df)} rows")
        else:
            print(f"   ❌ No data returned")
            return None

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    # Identify columns
    cohort_col = None
    period_col = None
    value_col = None

    print(f"   Available columns: {list(df.columns)}")

    for col in df.columns:
        col_lower = str(col).lower()
        if 'first transaction month' in col_lower or 'first_transaction_month' in col_lower:
            cohort_col = col
        elif 'period' in col_lower:
            period_col = col
        elif any(x in col_lower for x in ['contribution', 'profit', 'gtv', 'logo', 'count', 'loss', 'gross transaction value']):
            # Skip percentage columns (like "% of GTV" for net losses)
            if '%' in col_lower or 'percent' in col_lower or 'pct' in col_lower:
                print(f"   Skipping percentage column: {col}")
                continue
            # Skip ratio columns (like "net losses as % of gtv")
            if 'as %' in col_lower or 'ratio' in col_lower:
                print(f"   Skipping ratio column: {col}")
                continue
            value_col = col

    if not all([cohort_col, period_col, value_col]):
        print(f"   ❌ Missing columns")
        print(f"   Cohort: {cohort_col}, Period: {period_col}, Value: {value_col}")
        return None

    print(f"   ✓ Using value column: {value_col}")

    # Create pivot
    pivot = df.pivot_table(
        values=value_col,
        index=cohort_col,
        columns=period_col,
        aggfunc='sum',
        fill_value=0
    )

    print(f"   ✓ Pivot: {pivot.shape[0]} cohorts x {pivot.shape[1]} periods")

    return pivot


def create_cumulative_table(pivot):
    """Create cumulative table (for profit and net losses)"""
    cumulative = pivot.copy()
    current_date = datetime.now()

    for cohort in cumulative.index:
        cohort_str = str(cohort)

        try:
            if 'T' in cohort_str:
                cohort_date = pd.to_datetime(cohort_str.split('T')[0])
            else:
                cohort_date = pd.to_datetime(cohort_str)

            months_elapsed = (current_date.year - cohort_date.year) * 12 + (current_date.month - cohort_date.month) + 1

            row_values = pivot.loc[cohort].values
            cumulative_values = []
            running_sum = 0

            for period_idx, val in enumerate(row_values):
                period_num = period_idx + 1
                if period_num <= months_elapsed:
                    running_sum += val
                    cumulative_values.append(running_sum)
                else:
                    cumulative_values.append(np.nan)

            cumulative.loc[cohort] = cumulative_values

        except:
            cumulative.loc[cohort] = pivot.loc[cohort].cumsum()

    return cumulative


def create_retention_table(pivot):
    """Create retention % table (Period X / Period 1)"""
    retention = pivot.copy()

    for cohort in retention.index:
        period_1_value = pivot.loc[cohort].iloc[0]  # First period value

        if period_1_value > 0:
            # Divide each period by Period 1
            retention.loc[cohort] = pivot.loc[cohort] / period_1_value
        else:
            retention.loc[cohort] = np.nan

    return retention


# Fetch all data
print("\n" + "=" * 80)
print("FETCHING DATA FROM METABASE")
print("=" * 80)

profit_pivot = fetch_and_process_card(PROFIT_CARD_ID, "Organic Profit Data")
net_losses_pivot = fetch_and_process_card(NET_LOSSES_CARD_ID, "Organic Net Losses Data")
gtv_pivot = fetch_and_process_card(GTV_CARD_ID, "Organic GTV Data")
logo_pivot = fetch_and_process_card(LOGO_CARD_ID, "Organic Logo Data")

if profit_pivot is None:
    print("\n❌ Failed to fetch profit data")
    exit(1)

# Process profit data
print("\n4. Processing profit analysis...")
profit_cumulative = create_cumulative_table(profit_pivot)
print(f"   ✓ Profit cumulative created")

# Process net losses data
net_losses_cumulative = None
if net_losses_pivot is not None:
    net_losses_cumulative = create_cumulative_table(net_losses_pivot)
    print(f"   ✓ Net losses cumulative created")

# Match spend to cohorts
spend_matched = {}
for cohort in profit_pivot.index:
    cohort_str = str(cohort)

    try:
        if 'T' in cohort_str:
            cohort_date = pd.to_datetime(cohort_str.split('T')[0])
        else:
            cohort_date = pd.to_datetime(cohort_str)

        month_key = cohort_date.strftime('%Y-%m')

        if month_key in organic_spend:
            spend_matched[cohort] = organic_spend[month_key]

    except:
        pass

spend_series = pd.Series(spend_matched, name='Marketing Spend')

# Calculate payback ratios
profit_payback = profit_cumulative.copy()
for cohort in profit_payback.index:
    if cohort in spend_matched and spend_matched[cohort] > 0:
        spend = spend_matched[cohort]
        profit_payback.loc[cohort] = profit_cumulative.loc[cohort] / spend
    else:
        profit_payback.loc[cohort] = np.nan

print(f"   ✓ Payback calculated")

# Process GTV and Logo retention
gtv_retention = create_retention_table(gtv_pivot) if gtv_pivot is not None else None
logo_retention = create_retention_table(logo_pivot) if logo_pivot is not None else None

if gtv_retention is not None:
    print(f"   ✓ GTV retention calculated")
if logo_retention is not None:
    print(f"   ✓ Logo retention calculated")

# Keep raw logo counts as well (not retention %)
logo_counts = logo_pivot if logo_pivot is not None else None
if logo_counts is not None:
    print(f"   ✓ Logo counts preserved")

# Write to Excel
output_file = f'Organic_Retention_Analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

print(f"\n5. Creating Excel file: {output_file}")

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    from openpyxl.styles import numbers, Font

    ws_row = 0  # Track current row position

    # SECTION 1: Profit Cumulative
    profit_cumulative.to_excel(writer, sheet_name='Analysis', startrow=ws_row)
    ws = writer.sheets['Analysis']

    # Format cumulative (currency)
    for row in range(ws_row + 2, ws_row + profit_cumulative.shape[0] + 2):
        for col in range(2, profit_cumulative.shape[1] + 2):
            cell = ws.cell(row=row, column=col)
            cell.number_format = '$#,##0'

    ws_row += profit_cumulative.shape[0] + 3

    # SECTION 2: Profit Payback
    header_cell = ws.cell(row=ws_row, column=1)
    header_cell.value = "Profit Payback %"
    header_cell.font = Font(bold=True)

    profit_payback_with_spend = profit_payback.copy()
    profit_payback_with_spend.insert(0, 'Organic Spend', spend_series)
    profit_payback_with_spend.to_excel(writer, sheet_name='Analysis', startrow=ws_row + 1)

    # Format spend column (currency)
    for row in range(ws_row + 3, ws_row + profit_payback_with_spend.shape[0] + 3):
        cell = ws.cell(row=row, column=2)
        cell.number_format = '$#,##0'

    # Format payback ratios (percentage)
    for row in range(ws_row + 3, ws_row + profit_payback_with_spend.shape[0] + 3):
        for col in range(3, profit_payback_with_spend.shape[1] + 2):
            cell = ws.cell(row=row, column=col)
            cell.number_format = '0.00%'

    ws_row += profit_payback_with_spend.shape[0] + 4

    # SECTION 3: Net Losses Cumulative
    if net_losses_cumulative is not None:
        header_cell = ws.cell(row=ws_row, column=1)
        header_cell.value = "Net Losses Cumulative"
        header_cell.font = Font(bold=True)

        net_losses_cumulative.to_excel(writer, sheet_name='Analysis', startrow=ws_row + 1)

        # Format as currency
        for row in range(ws_row + 3, ws_row + net_losses_cumulative.shape[0] + 3):
            for col in range(2, net_losses_cumulative.shape[1] + 2):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '$#,##0'

        ws_row += net_losses_cumulative.shape[0] + 4

    # SECTION 4: GTV Retention
    if gtv_retention is not None:
        header_cell = ws.cell(row=ws_row, column=1)
        header_cell.value = "GTV Retention %"
        header_cell.font = Font(bold=True)

        gtv_retention.to_excel(writer, sheet_name='Analysis', startrow=ws_row + 1)

        # Format as percentage
        for row in range(ws_row + 3, ws_row + gtv_retention.shape[0] + 3):
            for col in range(2, gtv_retention.shape[1] + 2):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '0.00%'

        ws_row += gtv_retention.shape[0] + 4

    # SECTION 5: Logo Retention
    if logo_retention is not None:
        header_cell = ws.cell(row=ws_row, column=1)
        header_cell.value = "Logo Retention %"
        header_cell.font = Font(bold=True)

        logo_retention.to_excel(writer, sheet_name='Analysis', startrow=ws_row + 1)

        # Format as percentage
        for row in range(ws_row + 3, ws_row + logo_retention.shape[0] + 3):
            for col in range(2, logo_retention.shape[1] + 2):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '0.00%'

        ws_row += logo_retention.shape[0] + 4

    # SECTION 6: Logo Counts (Raw)
    if logo_counts is not None:
        header_cell = ws.cell(row=ws_row, column=1)
        header_cell.value = "Logo Counts (Raw)"
        header_cell.font = Font(bold=True)

        logo_counts.to_excel(writer, sheet_name='Analysis', startrow=ws_row + 1)

        # Format as whole numbers
        for row in range(ws_row + 3, ws_row + logo_counts.shape[0] + 3):
            for col in range(2, logo_counts.shape[1] + 2):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '#,##0'

        ws_row += logo_counts.shape[0] + 4

    print(f"   ✓ Exported all sections to 'Analysis' sheet")

print(f"\n✅ Complete!")
print(f"\nFile: {output_file}")
print(f"\nSheet contains:")
print(f"  - Profit cumulative ($)")
print(f"  - Profit payback (%)")
if net_losses_cumulative is not None:
    print(f"  - Net losses cumulative ($)")
if gtv_retention is not None:
    print(f"  - GTV retention (%)")
if logo_retention is not None:
    print(f"  - Logo retention (%)")
if logo_counts is not None:
    print(f"  - Logo counts (raw #)")
print("\n" + "=" * 80)
