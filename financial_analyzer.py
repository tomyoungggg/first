#!/usr/bin/env python3
"""
Financial Analyzer - Google Sheets Integration
Connects to Google Sheets, pulls financial data, and performs analysis.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import json

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Error: Required package not installed: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class GoogleSheetsFinancialAnalyzer:
    """Analyzes financial data from Google Sheets."""

    # Google Sheets API scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    def __init__(self, credentials_file='credentials.json', spreadsheet_name='2026 Budget [a.o. 12-25]'):
        """
        Initialize the analyzer.

        Args:
            credentials_file: Path to Google service account credentials JSON
            spreadsheet_name: Name of the Google Sheets spreadsheet
        """
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.service = None
        self.spreadsheet_id = None

    def authenticate(self):
        """Authenticate with Google Sheets API."""
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"Credentials file not found: {self.credentials_file}\n"
                f"Please follow the setup instructions in GOOGLE_SHEETS_SETUP.md"
            )

        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            print(f"✓ Successfully authenticated with Google Sheets API")
            return True
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            return False

    def find_spreadsheet(self):
        """Find the spreadsheet ID by name."""
        try:
            # Use Drive API to search for spreadsheet by name
            from googleapiclient.discovery import build

            # We need to use the service account credentials with Drive API
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            drive_service = build('drive', 'v3', credentials=credentials)

            # Search for the spreadsheet
            query = f"name='{self.spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'"
            results = drive_service.files().list(
                q=query,
                fields='files(id, name)',
                pageSize=10
            ).execute()

            files = results.get('files', [])

            if not files:
                raise ValueError(
                    f"Spreadsheet '{self.spreadsheet_name}' not found.\n"
                    f"Make sure:\n"
                    f"1. The spreadsheet name is correct\n"
                    f"2. You've shared the spreadsheet with the service account email"
                )

            self.spreadsheet_id = files[0]['id']
            print(f"✓ Found spreadsheet: {files[0]['name']}")
            return True

        except Exception as e:
            print(f"✗ Error finding spreadsheet: {e}")
            return False

    def get_sheet_data(self, sheet_range='A:Z'):
        """
        Fetch data from the spreadsheet.

        Args:
            sheet_range: Range to fetch (e.g., 'A:Z' or 'Sheet1!A1:D10')

        Returns:
            pandas DataFrame with the data
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_range
            ).execute()

            values = result.get('values', [])

            if not values:
                print("✗ No data found in spreadsheet")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            print(f"✓ Retrieved {len(df)} rows and {len(df.columns)} columns")
            return df

        except HttpError as e:
            print(f"✗ Error fetching data: {e}")
            return None

    def clean_currency_column(self, series):
        """Clean currency values from a pandas series."""
        if series.dtype == 'object':
            # Remove currency symbols and commas, convert to float
            cleaned = series.str.replace('$', '', regex=False)
            cleaned = cleaned.str.replace(',', '', regex=False)
            cleaned = cleaned.str.strip()
            # Handle empty strings
            cleaned = cleaned.replace('', '0')
            try:
                return pd.to_numeric(cleaned, errors='coerce')
            except:
                return series
        return series

    def analyze_financial_data(self, df):
        """
        Perform financial analysis on the data.

        Args:
            df: pandas DataFrame with financial data

        Returns:
            dict with analysis results
        """
        if df is None or df.empty:
            return None

        analysis = {
            'summary': {},
            'breakdown': {},
            'insights': []
        }

        print("\n" + "="*60)
        print("FINANCIAL ANALYSIS REPORT")
        print("="*60)
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data Source: {self.spreadsheet_name}")
        print("="*60)

        # Display basic info
        print(f"\n📊 Dataset Overview:")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"\n   Column Names:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")

        # Try to identify numeric columns for analysis
        print(f"\n💰 Analyzing Numeric Columns:")
        numeric_cols = []

        for col in df.columns:
            # Try to clean and convert to numeric
            cleaned = self.clean_currency_column(df[col])
            if pd.api.types.is_numeric_dtype(cleaned) and cleaned.notna().any():
                numeric_cols.append(col)
                df[col] = cleaned

        if numeric_cols:
            print(f"   Found {len(numeric_cols)} numeric columns:")
            for col in numeric_cols:
                print(f"   - {col}")

            # Calculate statistics for each numeric column
            print(f"\n📈 Statistical Summary:")
            for col in numeric_cols:
                values = df[col].dropna()
                if len(values) > 0:
                    total = values.sum()
                    mean = values.mean()
                    median = values.median()
                    std = values.std()
                    min_val = values.min()
                    max_val = values.max()

                    print(f"\n   {col}:")
                    print(f"      Total: ${total:,.2f}")
                    print(f"      Average: ${mean:,.2f}")
                    print(f"      Median: ${median:,.2f}")
                    print(f"      Std Dev: ${std:,.2f}")
                    print(f"      Min: ${min_val:,.2f}")
                    print(f"      Max: ${max_val:,.2f}")

                    analysis['breakdown'][col] = {
                        'total': float(total),
                        'average': float(mean),
                        'median': float(median),
                        'std_dev': float(std),
                        'min': float(min_val),
                        'max': float(max_val)
                    }

        # Look for category columns
        categorical_cols = [col for col in df.columns if col not in numeric_cols]

        if categorical_cols and numeric_cols:
            print(f"\n📂 Category Analysis:")
            # Try to do breakdown by categories
            for cat_col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                if df[cat_col].notna().any():
                    print(f"\n   Breakdown by '{cat_col}':")
                    for num_col in numeric_cols[:2]:  # Limit to first 2 numeric columns
                        grouped = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False)
                        if len(grouped) > 0 and len(grouped) < 50:  # Only show if reasonable number of categories
                            print(f"\n      {num_col} by {cat_col}:")
                            for idx, (category, value) in enumerate(grouped.head(10).items(), 1):
                                percentage = (value / grouped.sum() * 100) if grouped.sum() != 0 else 0
                                print(f"         {idx}. {category}: ${value:,.2f} ({percentage:.1f}%)")

        # Generate insights
        print(f"\n💡 Key Insights:")
        insights = []

        if numeric_cols:
            for col in numeric_cols:
                values = df[col].dropna()
                if len(values) > 0:
                    total = values.sum()
                    if total > 0:
                        insights.append(f"Total {col}: ${total:,.2f}")
                    elif total < 0:
                        insights.append(f"Net {col}: -${abs(total):,.2f} (deficit)")

        if insights:
            for i, insight in enumerate(insights, 1):
                print(f"   {i}. {insight}")
                analysis['insights'].append(insight)

        print("\n" + "="*60)

        return analysis

    def export_to_csv(self, df, output_file='financial_data_export.csv'):
        """Export the data to CSV file."""
        try:
            df.to_csv(output_file, index=False)
            print(f"✓ Data exported to: {output_file}")
            return True
        except Exception as e:
            print(f"✗ Error exporting to CSV: {e}")
            return False

    def run(self, sheet_range='A:Z', export_csv=True):
        """
        Run the complete analysis workflow.

        Args:
            sheet_range: Range to fetch from the sheet
            export_csv: Whether to export data to CSV
        """
        print("\n🚀 Starting Financial Analysis...")
        print("-" * 60)

        # Step 1: Authenticate
        if not self.authenticate():
            return False

        # Step 2: Find spreadsheet
        if not self.find_spreadsheet():
            return False

        # Step 3: Fetch data
        print(f"\n📥 Fetching data from range: {sheet_range}")
        df = self.get_sheet_data(sheet_range)

        if df is None:
            return False

        # Step 4: Analyze
        analysis = self.analyze_financial_data(df)

        # Step 5: Export
        if export_csv and df is not None:
            print(f"\n💾 Exporting data...")
            self.export_to_csv(df)

        print(f"\n✅ Analysis complete!\n")
        return True


def main():
    """Main entry point."""
    # You can customize these settings
    CREDENTIALS_FILE = os.path.expanduser('~/Desktop/credentials.json')
    SPREADSHEET_NAME = '2026 Budget [a.o. 12-25]'
    SHEET_RANGE = 'A:Z'  # Adjust this to your sheet range (e.g., 'Sheet1!A1:D100')

    # Create analyzer instance
    analyzer = GoogleSheetsFinancialAnalyzer(
        credentials_file=CREDENTIALS_FILE,
        spreadsheet_name=SPREADSHEET_NAME
    )

    # Run analysis
    try:
        analyzer.run(sheet_range=SHEET_RANGE, export_csv=True)
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
