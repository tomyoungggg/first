import pandas as pd
from datetime import datetime
import requests
from config import METABASE_URL, METABASE_API_KEY
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import numpy as np

print("=" * 80)
print("ACCOUNT EXECUTIVE PAYBACK ANALYSIS")
print("=" * 80)

AE_SHEET_ID = '1-kbUBDVdLIXf0bbG4C_c7JWbyipGQtCdWjW7R7agiaM'
CREDENTIALS_FILE = r'C:\Users\Tom Young\OneDrive\Desktop\credentials.json'
AE_CARD_ID = 13796

metabase_headers = {
    "X-API-KEY": METABASE_API_KEY,
    "Content-Type": "application/json"
}

# Step 1: Fetch AE cost data from Google Sheet
print("\n1. Fetching AE cost data from Google Sheet...")

try:
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=credentials)

    # Read Account Executives tab (plural!)
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=AE_SHEET_ID,
        range="'Account Executives'!B3:G100"
    ).execute()

    values = result.get('values', [])

    ae_costs = {}

    for row in values:
        if len(row) < 6:
            continue

        ae_name = row[0]  # Column B
        monthly_wages_str = row[3]  # Column E
        monthly_te_str = row[4]  # Column F
        bonus_format_str = row[5]  # Column G

        if not ae_name or not monthly_wages_str or not monthly_te_str:
            continue

        try:
            monthly_wages = float(str(monthly_wages_str).replace('$', '').replace(',', '').strip())
            monthly_te = float(str(monthly_te_str).replace('$', '').replace(',', '').strip())

            # Parse bonus percentage (e.g., "10%" -> 0.10)
            bonus_pct = 0
            if bonus_format_str and '%' in str(bonus_format_str):
                bonus_pct = float(str(bonus_format_str).replace('%', '').strip()) / 100

            ae_costs[ae_name] = {
                'monthly_wages': monthly_wages,
                'monthly_te': monthly_te,
                'bonus_pct': bonus_pct
            }

            print(f"   {ae_name}: Wages=${monthly_wages:,.0f}, T&E=${monthly_te:,.0f}, Bonus={bonus_pct:.0%}")

        except Exception as e:
            print(f"   ⚠ Error parsing {ae_name}: {e}")
            continue

    print(f"\n   ✓ Loaded costs for {len(ae_costs)} active AEs")

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    ae_costs = {}

if not ae_costs:
    print("\n❌ No AE cost data loaded")
    exit(1)

# Step 2: Fetch AE retention data from Metabase
print("\n2. Fetching AE retention data from Metabase...")

try:
    response = requests.post(
        f"{METABASE_URL}/api/card/{AE_CARD_ID}/query/json",
        headers=metabase_headers
    )
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        print(f"   ✓ Retrieved {len(df)} rows, {len(df.columns)} columns")
        print(f"   Columns: {list(df.columns)}")
    else:
        print(f"   ❌ No data returned")
        exit(1)

except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Step 3: Identify columns
ae_col = None
cohort_col = None
period_col = None
value_col = None

for col in df.columns:
    col_lower = str(col).lower()
    if 'account executive' in col_lower or 'account_executive' in col_lower:
        ae_col = col
    elif 'first transaction month' in col_lower or 'first_transaction_month' in col_lower:
        cohort_col = col
    elif 'period' in col_lower:
        period_col = col
    elif 'contribution' in col_lower or 'profit' in col_lower:
        value_col = col

if not all([ae_col, cohort_col, period_col, value_col]):
    print(f"\n❌ Missing required columns")
    print(f"   AE column: {ae_col}")
    print(f"   Cohort column: {cohort_col}")
    print(f"   Period column: {period_col}")
    print(f"   Value column: {value_col}")
    exit(1)

print(f"\n   ✓ Identified columns:")
print(f"     AE: {ae_col}")
print(f"     Cohort: {cohort_col}")
print(f"     Period: {period_col}")
print(f"     Value: {value_col}")

# Step 4: Create Excel with ONE tab per AE
output_file = f'AE_Payback_Analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

print(f"\n3. Creating Excel file: {output_file}")

current_date = datetime.now()

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

    # Process each active AE
    for ae_name, costs in ae_costs.items():

        print(f"\n   Processing: {ae_name}")

        # Filter data for this AE
        ae_df = df[df[ae_col] == ae_name].copy()

        if ae_df.empty:
            print(f"     ⚠ No data found for {ae_name} in Metabase")
            continue

        print(f"     ✓ Found {len(ae_df)} rows")

        # Create pivot
        try:
            pivot = ae_df.pivot_table(
                values=value_col,
                index=cohort_col,
                columns=period_col,
                aggfunc='sum',
                fill_value=0
            )
        except Exception as e:
            print(f"     ⚠ Error creating pivot: {e}")
            continue

        print(f"     ✓ Pivot: {pivot.shape[0]} cohorts x {pivot.shape[1]} periods")

        # Create cumulative
        cumulative = pivot.copy()

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

        print(f"     ✓ Cumulative pivot created")

        # Calculate costs for each cohort
        monthly_wages = costs['monthly_wages']
        monthly_te = costs['monthly_te']
        bonus_pct = costs['bonus_pct']

        # Get latest cumulative value for each cohort (for bonus calculation)
        latest_cumulative = cumulative.apply(lambda row: row.dropna().iloc[-1] if len(row.dropna()) > 0 else 0, axis=1)

        # Calculate bonus cost
        bonus_costs = latest_cumulative * bonus_pct

        # Total acquisition cost per cohort
        base_cost = monthly_wages + monthly_te
        total_costs = base_cost + bonus_costs

        # Create cost breakdown DataFrame
        cost_breakdown = pd.DataFrame({
            'Monthly Wages': monthly_wages,
            'Monthly T&E': monthly_te,
            'Bonus Cost': bonus_costs,
            'Total Acq Cost': total_costs
        }, index=cumulative.index)

        # Calculate payback ratios
        payback = cumulative.copy()
        for cohort in payback.index:
            if total_costs[cohort] > 0:
                payback.loc[cohort] = cumulative.loc[cohort] / total_costs[cohort]
            else:
                payback.loc[cohort] = np.nan

        print(f"     ✓ Cost analysis complete")

        # Create sheet name (clean for Excel)
        sheet_name = ae_name[:31].replace('/', '-').replace('\\', '-')

        # Write to ONE tab: cumulative at top, payback below
        # Write cumulative first
        cumulative.to_excel(writer, sheet_name=sheet_name, startrow=0)

        # Write payback with cost breakdown below (with spacing)
        payback_start_row = cumulative.shape[0] + 3

        # Combine cost breakdown with payback ratios
        payback_with_costs = payback.copy()
        for col in ['Total Acq Cost', 'Bonus Cost', 'Monthly T&E', 'Monthly Wages']:
            payback_with_costs.insert(0, col, cost_breakdown[col])

        payback_with_costs.to_excel(writer, sheet_name=sheet_name, startrow=payback_start_row)

        # Format
        from openpyxl.styles import numbers, Font

        ws = writer.sheets[sheet_name]

        # Format cumulative section (currency)
        for row in range(2, cumulative.shape[0] + 2):
            for col in range(2, cumulative.shape[1] + 2):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '$#,##0'

        # Add "Payback Analysis" header
        header_cell = ws.cell(row=payback_start_row, column=1)
        header_cell.value = "Payback Analysis"
        header_cell.font = Font(bold=True)

        # Format payback section - cost columns as currency (columns 2-5)
        for row in range(payback_start_row + 2, payback_start_row + payback_with_costs.shape[0] + 2):
            for col in range(2, 6):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '$#,##0'

        # Format payback ratios as percentage (columns 6+)
        for row in range(payback_start_row + 2, payback_start_row + payback_with_costs.shape[0] + 2):
            for col in range(6, payback_with_costs.shape[1] + 2):
                cell = ws.cell(row=row, column=col)
                cell.number_format = '0.00%'

        print(f"     ✓ Exported 1 consolidated tab for {ae_name}")

print(f"\n✅ Complete!")
print(f"\nFile: {output_file}")
print(f"\nCreated tabs for {len(ae_costs)} Account Executives")
print(f"\nEach tab contains:")
print(f"  - Cumulative tracking (top)")
print(f"  - Payback analysis with costs (below)")
print("\n" + "=" * 80)
