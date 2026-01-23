# Google Sheets API Setup Instructions

This guide will help you set up Google Sheets API access for the financial analyzer script.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Financial Analyzer")
5. Click "Create"

## Step 2: Enable Google Sheets API

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on "Google Sheets API"
4. Click "Enable"

## Step 3: Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Enter a service account name (e.g., "sheets-analyzer")
4. Click "Create and Continue"
5. Skip the optional steps by clicking "Continue" and then "Done"
6. Click on the newly created service account email
7. Go to the "Keys" tab
8. Click "Add Key" > "Create new key"
9. Select "JSON" format
10. Click "Create"
11. A JSON file will be downloaded - **save this file securely**

## Step 4: Configure the Script

1. Rename the downloaded JSON file to `credentials.json`
2. Move it to the same directory as `financial_analyzer.py`
3. Update the `config.py` file with your spreadsheet details:
   - `SPREADSHEET_NAME`: The name of your Google Sheets file
   - `SHEET_NAME`: The specific sheet/tab name (optional, defaults to first sheet)

## Step 5: Share Your Spreadsheet with the Service Account

**IMPORTANT**: You must share your Google Sheets spreadsheet with the service account email address.

1. Open your Google Sheets spreadsheet ('2026 Budget [a.o. 12-25]')
2. Click the "Share" button
3. Copy the service account email from the `credentials.json` file (it looks like: `your-service-account@project-id.iam.gserviceaccount.com`)
4. Paste the email in the "Share with people and groups" field
5. Set permission to "Viewer" (read-only access)
6. Uncheck "Notify people" (optional)
7. Click "Share"

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Run the Script

```bash
python financial_analyzer.py
```

## Security Notes

- **Never commit `credentials.json` to version control**
- The `credentials.json` file is already in `.gitignore`
- Keep your credentials secure and don't share them
- Consider using environment variables for production deployments

## Troubleshooting

### Error: "Credentials file not found"
- Make sure `credentials.json` is in the same directory as the script
- Check that the file is named correctly

### Error: "The caller does not have permission"
- Make sure you've shared the spreadsheet with the service account email
- Check that the spreadsheet name in `config.py` matches exactly

### Error: "Spreadsheet not found"
- Verify the spreadsheet name is correct (case-sensitive)
- Ensure the spreadsheet is shared with the service account
