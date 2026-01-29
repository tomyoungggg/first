# Sales Tax Hub Documents

This folder is for storing all relevant sales tax documents, templates, and resources that will be linked from the Sales Tax Hub.

## Folder Structure

```
documents/
├── guides/              # How-to guides and documentation
├── policies/            # Company policies and procedures
├── templates/           # Forms and certificate templates
├── training/            # Training materials and presentations
├── state-info/          # State-specific information and guides
└── exemption-forms/     # Exemption certificate templates by state
```

## How to Add Documents

1. Place your document in the appropriate subfolder
2. Use clear, descriptive filenames (e.g., `california-sales-tax-guide.pdf`)
3. Update the relevant links in `index.html` to point to your document

## Naming Conventions

- Use lowercase letters
- Replace spaces with hyphens (`-`)
- Include version or date if applicable (e.g., `exemption-policy-2026.pdf`)
- Use descriptive names that indicate the content

## Supported File Types

- PDF documents (`.pdf`)
- Word documents (`.docx`)
- Excel spreadsheets (`.xlsx`)
- PowerPoint presentations (`.pptx`)
- Images (`.png`, `.jpg`)
- Markdown files (`.md`)

## Linking Documents

To link a document from the hub, update the href in `index.html`:

```html
<a href="documents/guides/your-document.pdf">Document Title</a>
```

## Alternative: Cloud Storage Integration

For dynamic document management, consider integrating with:

- **Google Drive** - Share a folder and embed links
- **Notion** - Create a knowledge base with embedded docs
- **Confluence** - Enterprise wiki with document management
- **SharePoint** - Microsoft document management

To integrate cloud storage, simply replace the document links in `index.html` with your cloud storage URLs.

## Questions?

Contact the tax team at tax@whop.com for assistance.
