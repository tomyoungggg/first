"""
Configuration file for Metabase Analysis Tools
Copy this file to config.py and fill in your actual values
"""

# Metabase Configuration
METABASE_URL = "https://whop.metabaseapp.com"
METABASE_API_KEY = "your-api-key-here"
DASHBOARD_ID = 2773

# Gmail Configuration (if using email features)
GMAIL_USER = "your-email@company.com"
GMAIL_APP_PASSWORD = "your-app-password-here"

# Email Recipients (if using email features)
RECIPIENTS = [
    # "person1@company.com",
    # "person2@company.com",
]

# Report Configuration
REPORT_TITLE = "GTM Cohort LTV vs CAC Report"
REPORT_FREQUENCY = "weekly"  # Options: daily, weekly, monthly

# Metrics to track
METRICS = {
    "ltv_threshold": 100000,  # $100k threshold
    "cac_goal": 0.3,  # Target LTV/CAC ratio (e.g., 3:1)
}
