# Whop Sales Tax Hub

An internal resource hub for all things sales tax at Whop. This single-page application provides quick access to tax information, tools, resources, and contacts.

## Features

### Dashboard
- Key metrics overview (states registered, YTD tax collected, etc.)
- Quick action buttons for common tasks
- Upcoming filing deadlines with urgency indicators
- Recent updates and announcements

### State Directory
- Complete list of all US states with tax information
- Registration status (Registered, Pending, Not Required)
- State tax rates and filing frequencies
- Economic nexus thresholds
- Filter and search functionality

### Resources & Documentation
- Guides and how-tos
- Policies and procedures
- FAQs
- Templates and forms
- Training materials
- External resource links

### Tools & Calculators
- **Tax Rate Calculator** - Look up combined tax rates by address
- **Tax Amount Calculator** - Calculate tax for a given price and rate
- **Nexus Threshold Checker** - Check if nexus thresholds are met in specific states
- **Product Taxability Lookup** - Check if product categories are taxable by state

### Contacts
- Key team members and their areas of expertise
- External partners (e.g., Avalara)
- Escalation path for issues

## Getting Started

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sales-tax-hub
   ```

2. Open the site locally:
   ```bash
   # Using Python
   python -m http.server 8000

   # Using Node.js (npx)
   npx serve

   # Or simply open index.html in a browser
   open index.html
   ```

3. Visit `http://localhost:8000` in your browser

### Deployment

This is a static site that can be deployed to any web hosting service:

- **GitHub Pages** - Push to a `gh-pages` branch
- **Netlify** - Connect repo for automatic deployments
- **Vercel** - Connect repo for automatic deployments
- **AWS S3** - Upload files to an S3 bucket with static hosting
- **Internal Server** - Place files on any web server

## Project Structure

```
sales-tax-hub/
├── index.html           # Main HTML file
├── styles.css           # All CSS styles
├── app.js               # JavaScript functionality
├── README.md            # This file
└── documents/           # Document storage
    ├── guides/          # How-to guides
    ├── policies/        # Company policies
    ├── templates/       # Forms and templates
    ├── training/        # Training materials
    ├── state-info/      # State-specific docs
    └── exemption-forms/ # Exemption certificates
```

## Customization

### Updating State Data

Edit the `statesData` array in `app.js` to update:
- Registration status
- Tax rates
- Filing frequencies
- Nexus thresholds

### Adding Documents

1. Place documents in the appropriate `documents/` subfolder
2. Update links in `index.html` to point to the new documents

### Modifying Styles

All styles are in `styles.css`. Key customization points:
- CSS variables at the top for colors and spacing
- Section-specific styles are clearly labeled

### Adding New Sections

1. Add a new `<section>` in `index.html`
2. Add a navigation link in the navbar
3. Update `initNavigation()` in `app.js` if needed

## Updating Content

### Dashboard Stats
Update the stat values in `index.html` or make them dynamic by modifying `app.js`.

### Deadlines
Update the deadlines in the HTML or create a data structure in `app.js` to manage them.

### Contacts
Edit the contacts section in `index.html` with actual team member information.

### Updates/Announcements
Add new update cards to the updates section in `index.html`.

## Future Enhancements

Potential improvements:
- Backend API integration for dynamic data
- User authentication for sensitive information
- Real-time tax rate lookups via Avalara API
- Document upload functionality
- Calendar integration for deadline reminders
- Slack notifications for filing reminders

## Support

For questions or issues, contact the tax team:
- Email: tax@whop.com
- Slack: #tax-team
