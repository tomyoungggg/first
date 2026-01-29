// State Data
const statesData = [
    { name: 'Alabama', abbr: 'AL', status: 'registered', rate: '4.00%', filingFreq: 'Monthly', nexusThreshold: '$250,000', transactionThreshold: null },
    { name: 'Alaska', abbr: 'AK', status: 'not-required', rate: '0.00%', filingFreq: 'N/A', nexusThreshold: 'N/A', transactionThreshold: null },
    { name: 'Arizona', abbr: 'AZ', status: 'registered', rate: '5.60%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Arkansas', abbr: 'AR', status: 'registered', rate: '6.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'California', abbr: 'CA', status: 'registered', rate: '7.25%', filingFreq: 'Monthly', nexusThreshold: '$500,000', transactionThreshold: null },
    { name: 'Colorado', abbr: 'CO', status: 'registered', rate: '2.90%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Connecticut', abbr: 'CT', status: 'registered', rate: '6.35%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Delaware', abbr: 'DE', status: 'not-required', rate: '0.00%', filingFreq: 'N/A', nexusThreshold: 'N/A', transactionThreshold: null },
    { name: 'Florida', abbr: 'FL', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Georgia', abbr: 'GA', status: 'registered', rate: '4.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Hawaii', abbr: 'HI', status: 'registered', rate: '4.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Idaho', abbr: 'ID', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Illinois', abbr: 'IL', status: 'registered', rate: '6.25%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Indiana', abbr: 'IN', status: 'registered', rate: '7.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Iowa', abbr: 'IA', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Kansas', abbr: 'KS', status: 'registered', rate: '6.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Kentucky', abbr: 'KY', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Louisiana', abbr: 'LA', status: 'registered', rate: '4.45%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Maine', abbr: 'ME', status: 'registered', rate: '5.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Maryland', abbr: 'MD', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Massachusetts', abbr: 'MA', status: 'registered', rate: '6.25%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Michigan', abbr: 'MI', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Minnesota', abbr: 'MN', status: 'registered', rate: '6.875%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Mississippi', abbr: 'MS', status: 'registered', rate: '7.00%', filingFreq: 'Monthly', nexusThreshold: '$250,000', transactionThreshold: null },
    { name: 'Missouri', abbr: 'MO', status: 'registered', rate: '4.225%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Montana', abbr: 'MT', status: 'pending', rate: '0.00%', filingFreq: 'N/A', nexusThreshold: 'N/A', transactionThreshold: null },
    { name: 'Nebraska', abbr: 'NE', status: 'registered', rate: '5.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Nevada', abbr: 'NV', status: 'registered', rate: '6.85%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'New Hampshire', abbr: 'NH', status: 'not-required', rate: '0.00%', filingFreq: 'N/A', nexusThreshold: 'N/A', transactionThreshold: null },
    { name: 'New Jersey', abbr: 'NJ', status: 'registered', rate: '6.625%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'New Mexico', abbr: 'NM', status: 'registered', rate: '4.875%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'New York', abbr: 'NY', status: 'registered', rate: '4.00%', filingFreq: 'Quarterly', nexusThreshold: '$500,000', transactionThreshold: '100' },
    { name: 'North Carolina', abbr: 'NC', status: 'registered', rate: '4.75%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'North Dakota', abbr: 'ND', status: 'registered', rate: '5.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Ohio', abbr: 'OH', status: 'registered', rate: '5.75%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Oklahoma', abbr: 'OK', status: 'registered', rate: '4.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Oregon', abbr: 'OR', status: 'not-required', rate: '0.00%', filingFreq: 'N/A', nexusThreshold: 'N/A', transactionThreshold: null },
    { name: 'Pennsylvania', abbr: 'PA', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Rhode Island', abbr: 'RI', status: 'registered', rate: '7.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'South Carolina', abbr: 'SC', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'South Dakota', abbr: 'SD', status: 'registered', rate: '4.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Tennessee', abbr: 'TN', status: 'registered', rate: '7.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Texas', abbr: 'TX', status: 'registered', rate: '6.25%', filingFreq: 'Monthly', nexusThreshold: '$500,000', transactionThreshold: null },
    { name: 'Utah', abbr: 'UT', status: 'registered', rate: '6.10%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Vermont', abbr: 'VT', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Virginia', abbr: 'VA', status: 'registered', rate: '5.30%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Washington', abbr: 'WA', status: 'registered', rate: '6.50%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'West Virginia', abbr: 'WV', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Wisconsin', abbr: 'WI', status: 'registered', rate: '5.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: null },
    { name: 'Wyoming', abbr: 'WY', status: 'registered', rate: '4.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' },
    { name: 'Washington D.C.', abbr: 'DC', status: 'registered', rate: '6.00%', filingFreq: 'Monthly', nexusThreshold: '$100,000', transactionThreshold: '200' }
];

// Digital product taxability by state (simplified)
const taxabilityRules = {
    'digital-course': {
        'CA': { taxable: false, notes: 'Digital courses are exempt in California' },
        'TX': { taxable: true, notes: 'Digital courses are taxable in Texas' },
        'NY': { taxable: true, notes: 'Digital courses are taxable in New York' },
        'FL': { taxable: false, notes: 'Digital courses are exempt in Florida' },
        'WA': { taxable: true, notes: 'Digital courses are taxable in Washington' },
        'default': { taxable: 'varies', notes: 'Taxability varies - consult state-specific rules' }
    },
    'software-saas': {
        'CA': { taxable: false, notes: 'SaaS is exempt in California' },
        'TX': { taxable: true, notes: 'SaaS is taxable as data processing in Texas' },
        'NY': { taxable: true, notes: 'SaaS is taxable in New York' },
        'FL': { taxable: false, notes: 'SaaS is exempt in Florida' },
        'WA': { taxable: true, notes: 'SaaS is taxable in Washington' },
        'default': { taxable: 'varies', notes: 'Taxability varies - consult state-specific rules' }
    },
    'ebook': {
        'CA': { taxable: false, notes: 'eBooks are exempt in California' },
        'TX': { taxable: false, notes: 'eBooks are exempt in Texas' },
        'NY': { taxable: false, notes: 'eBooks are exempt in New York' },
        'FL': { taxable: false, notes: 'eBooks are exempt in Florida' },
        'WA': { taxable: true, notes: 'Digital products including eBooks are taxable in Washington' },
        'default': { taxable: 'varies', notes: 'Taxability varies - consult state-specific rules' }
    },
    'digital-download': {
        'CA': { taxable: false, notes: 'Digital downloads are exempt in California' },
        'TX': { taxable: true, notes: 'Digital downloads are taxable in Texas' },
        'NY': { taxable: true, notes: 'Digital downloads are taxable in New York' },
        'FL': { taxable: false, notes: 'Digital downloads are exempt in Florida' },
        'WA': { taxable: true, notes: 'Digital downloads are taxable in Washington' },
        'default': { taxable: 'varies', notes: 'Taxability varies - consult state-specific rules' }
    },
    'membership': {
        'CA': { taxable: false, notes: 'Memberships for digital access are generally exempt in California' },
        'TX': { taxable: true, notes: 'Memberships may be taxable in Texas depending on what is provided' },
        'NY': { taxable: true, notes: 'Memberships for digital content are generally taxable in New York' },
        'FL': { taxable: false, notes: 'Digital memberships are generally exempt in Florida' },
        'WA': { taxable: true, notes: 'Digital memberships are taxable in Washington' },
        'default': { taxable: 'varies', notes: 'Taxability depends on membership benefits - consult tax team' }
    },
    'consulting': {
        'CA': { taxable: false, notes: 'Professional services are exempt in California' },
        'TX': { taxable: false, notes: 'Professional services are exempt in Texas' },
        'NY': { taxable: false, notes: 'Consulting services are exempt in New York' },
        'FL': { taxable: false, notes: 'Professional services are exempt in Florida' },
        'WA': { taxable: false, notes: 'Professional services are exempt in Washington' },
        'default': { taxable: false, notes: 'Consulting services are generally not taxable' }
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    populateStates();
    populateStateDropdowns();
    initSearch();
    initFilters();
});

// Navigation
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);

            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');

            // Show target section
            sections.forEach(section => {
                if (section.id === targetId) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}

// Populate states grid
function populateStates(filter = 'all', search = '') {
    const grid = document.getElementById('statesGrid');
    grid.innerHTML = '';

    let filteredStates = statesData;

    // Apply status filter
    if (filter !== 'all') {
        filteredStates = filteredStates.filter(state => state.status === filter);
    }

    // Apply search filter
    if (search) {
        const searchLower = search.toLowerCase();
        filteredStates = filteredStates.filter(state =>
            state.name.toLowerCase().includes(searchLower) ||
            state.abbr.toLowerCase().includes(searchLower)
        );
    }

    filteredStates.forEach(state => {
        const card = document.createElement('div');
        card.className = 'state-card';
        card.innerHTML = `
            <div class="state-header">
                <div>
                    <div class="state-name">${state.name}</div>
                    <span class="state-abbr">${state.abbr}</span>
                </div>
                <span class="state-status ${state.status}">${formatStatus(state.status)}</span>
            </div>
            <div class="state-details">
                <div class="state-detail">
                    <span class="state-detail-label">State Tax Rate</span>
                    <span class="state-detail-value">${state.rate}</span>
                </div>
                <div class="state-detail">
                    <span class="state-detail-label">Filing Frequency</span>
                    <span class="state-detail-value">${state.filingFreq}</span>
                </div>
                <div class="state-detail">
                    <span class="state-detail-label">Nexus Threshold</span>
                    <span class="state-detail-value">${state.nexusThreshold}</span>
                </div>
                ${state.transactionThreshold ? `
                <div class="state-detail">
                    <span class="state-detail-label">Transaction Threshold</span>
                    <span class="state-detail-value">${state.transactionThreshold} transactions</span>
                </div>
                ` : ''}
            </div>
        `;
        grid.appendChild(card);
    });

    if (filteredStates.length === 0) {
        grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px;">No states found matching your criteria.</p>';
    }
}

function formatStatus(status) {
    const statusMap = {
        'registered': 'Registered',
        'pending': 'Pending',
        'not-required': 'Not Required'
    };
    return statusMap[status] || status;
}

// Populate state dropdowns
function populateStateDropdowns() {
    const dropdowns = ['nexusState', 'taxabilityState'];

    dropdowns.forEach(dropdownId => {
        const dropdown = document.getElementById(dropdownId);
        if (dropdown) {
            statesData.forEach(state => {
                const option = document.createElement('option');
                option.value = state.abbr;
                option.textContent = state.name;
                dropdown.appendChild(option);
            });
        }
    });
}

// Initialize search
function initSearch() {
    const globalSearch = document.getElementById('globalSearch');
    if (globalSearch) {
        globalSearch.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            // For now, navigate to states and search there
            if (searchTerm.length > 0) {
                document.querySelector('[href="#states"]').click();
                document.getElementById('stateSearch').value = searchTerm;
                populateStates('all', searchTerm);
            }
        });
    }
}

// Initialize filters
function initFilters() {
    const statusFilter = document.getElementById('stateStatusFilter');
    const stateSearch = document.getElementById('stateSearch');

    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            const search = stateSearch ? stateSearch.value : '';
            populateStates(this.value, search);
        });
    }

    if (stateSearch) {
        stateSearch.addEventListener('input', function() {
            const filter = statusFilter ? statusFilter.value : 'all';
            populateStates(filter, this.value);
        });
    }
}

// Modal functions
function openModal(type) {
    const overlay = document.getElementById('modalOverlay');
    const content = document.getElementById('modalContent');

    let modalHTML = '';

    switch(type) {
        case 'newExemption':
            modalHTML = `
                <h2>New Exemption Certificate</h2>
                <p>Submit a new exemption certificate for processing.</p>
                <form class="modal-form" onsubmit="handleFormSubmit(event, 'exemption')">
                    <div class="form-group">
                        <label>Customer Name</label>
                        <input type="text" required placeholder="Enter customer name">
                    </div>
                    <div class="form-group">
                        <label>Customer Email</label>
                        <input type="email" required placeholder="Enter customer email">
                    </div>
                    <div class="form-group">
                        <label>State(s)</label>
                        <input type="text" required placeholder="e.g., CA, TX, NY">
                    </div>
                    <div class="form-group">
                        <label>Exemption Type</label>
                        <select required>
                            <option value="">Select type...</option>
                            <option value="resale">Resale Certificate</option>
                            <option value="nonprofit">Non-Profit Exemption</option>
                            <option value="government">Government Entity</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Notes</label>
                        <textarea placeholder="Additional notes..."></textarea>
                    </div>
                    <button type="submit" class="btn-primary">Submit Certificate</button>
                </form>
            `;
            break;

        case 'taxLookup':
            modalHTML = `
                <h2>Tax Rate Lookup</h2>
                <p>Look up the tax rate for a specific address.</p>
                <form class="modal-form" onsubmit="handleFormSubmit(event, 'lookup')">
                    <div class="form-group">
                        <label>Street Address</label>
                        <input type="text" required placeholder="123 Main St">
                    </div>
                    <div class="form-group">
                        <label>City</label>
                        <input type="text" required placeholder="City name">
                    </div>
                    <div class="form-group">
                        <label>State</label>
                        <select required>
                            <option value="">Select state...</option>
                            ${statesData.map(s => `<option value="${s.abbr}">${s.name}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>ZIP Code</label>
                        <input type="text" required placeholder="12345" maxlength="10">
                    </div>
                    <button type="submit" class="btn-primary">Look Up Rate</button>
                </form>
            `;
            break;

        case 'reportIssue':
            modalHTML = `
                <h2>Report Tax Issue</h2>
                <p>Report a tax-related issue or discrepancy.</p>
                <form class="modal-form" onsubmit="handleFormSubmit(event, 'issue')">
                    <div class="form-group">
                        <label>Issue Type</label>
                        <select required>
                            <option value="">Select type...</option>
                            <option value="incorrect-rate">Incorrect Tax Rate</option>
                            <option value="wrong-calculation">Wrong Tax Calculation</option>
                            <option value="missing-exemption">Missing Exemption</option>
                            <option value="customer-dispute">Customer Dispute</option>
                            <option value="filing-error">Filing Error</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Order/Transaction ID</label>
                        <input type="text" placeholder="If applicable">
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <textarea required placeholder="Describe the issue in detail..."></textarea>
                    </div>
                    <div class="form-group">
                        <label>Priority</label>
                        <select required>
                            <option value="low">Low</option>
                            <option value="medium" selected>Medium</option>
                            <option value="high">High</option>
                            <option value="urgent">Urgent</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary">Submit Issue</button>
                </form>
            `;
            break;

        case 'requestHelp':
            modalHTML = `
                <h2>Request Help</h2>
                <p>Need assistance with a sales tax question? We're here to help.</p>
                <form class="modal-form" onsubmit="handleFormSubmit(event, 'help')">
                    <div class="form-group">
                        <label>Your Name</label>
                        <input type="text" required placeholder="Enter your name">
                    </div>
                    <div class="form-group">
                        <label>Your Email</label>
                        <input type="email" required placeholder="Enter your email">
                    </div>
                    <div class="form-group">
                        <label>Category</label>
                        <select required>
                            <option value="">Select category...</option>
                            <option value="general">General Question</option>
                            <option value="exemption">Exemption Certificate</option>
                            <option value="rate">Tax Rate Question</option>
                            <option value="filing">Filing/Compliance</option>
                            <option value="customer">Customer Issue</option>
                            <option value="technical">Technical/System Issue</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Question/Request</label>
                        <textarea required placeholder="How can we help you?"></textarea>
                    </div>
                    <button type="submit" class="btn-primary">Submit Request</button>
                </form>
            `;
            break;
    }

    content.innerHTML = modalHTML;
    overlay.classList.add('active');
}

function closeModal() {
    const overlay = document.getElementById('modalOverlay');
    overlay.classList.remove('active');
}

// Close modal on overlay click
document.getElementById('modalOverlay')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Close modal on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Form submission handler
function handleFormSubmit(event, type) {
    event.preventDefault();

    // In a real app, this would send data to a backend
    const messages = {
        'exemption': 'Exemption certificate submitted successfully! The tax team will review it within 2 business days.',
        'lookup': 'Tax rate lookup complete. Results have been logged.',
        'issue': 'Issue reported successfully! The tax team has been notified and will follow up.',
        'help': 'Help request submitted! Someone from the tax team will respond within 24 hours.'
    };

    alert(messages[type] || 'Form submitted successfully!');
    closeModal();
}

// Tool functions
function calculateTaxRate() {
    const street = document.getElementById('calcStreet').value;
    const city = document.getElementById('calcCity').value;
    const state = document.getElementById('calcState').value.toUpperCase();
    const zip = document.getElementById('calcZip').value;

    const resultDiv = document.getElementById('taxRateResult');

    if (!street || !city || !state || !zip) {
        resultDiv.innerHTML = 'Please fill in all fields.';
        resultDiv.className = 'tool-result show warning';
        return;
    }

    // Find state data
    const stateData = statesData.find(s => s.abbr === state);

    if (!stateData) {
        resultDiv.innerHTML = 'State not found. Please enter a valid state abbreviation.';
        resultDiv.className = 'tool-result show warning';
        return;
    }

    // Simulated calculation (in a real app, this would call a tax API)
    const baseRate = parseFloat(stateData.rate);
    const estimatedLocalRate = Math.random() * 3; // Random local rate for demo
    const totalRate = baseRate + estimatedLocalRate;

    resultDiv.innerHTML = `
        <strong>Estimated Tax Rate for ${city}, ${state} ${zip}</strong><br><br>
        State Rate: ${stateData.rate}<br>
        Est. Local Rate: ${estimatedLocalRate.toFixed(3)}%<br>
        <strong>Total Rate: ${totalRate.toFixed(3)}%</strong><br><br>
        <em>Note: For accurate rates, please use Avalara or consult the tax team.</em>
    `;
    resultDiv.className = 'tool-result show info';
}

function calculateTaxAmount() {
    const price = parseFloat(document.getElementById('calcPrice').value);
    const rate = parseFloat(document.getElementById('calcRate').value);

    const resultDiv = document.getElementById('taxAmountResult');

    if (isNaN(price) || isNaN(rate)) {
        resultDiv.innerHTML = 'Please enter valid numbers for price and rate.';
        resultDiv.className = 'tool-result show warning';
        return;
    }

    const taxAmount = price * (rate / 100);
    const total = price + taxAmount;

    resultDiv.innerHTML = `
        <strong>Tax Calculation Results</strong><br><br>
        Original Price: $${price.toFixed(2)}<br>
        Tax Rate: ${rate}%<br>
        Tax Amount: <strong>$${taxAmount.toFixed(2)}</strong><br>
        Total with Tax: <strong>$${total.toFixed(2)}</strong>
    `;
    resultDiv.className = 'tool-result show success';
}

function checkNexus() {
    const stateAbbr = document.getElementById('nexusState').value;
    const sales = parseFloat(document.getElementById('nexusSales').value);
    const transactions = parseInt(document.getElementById('nexusTransactions').value);

    const resultDiv = document.getElementById('nexusResult');

    if (!stateAbbr) {
        resultDiv.innerHTML = 'Please select a state.';
        resultDiv.className = 'tool-result show warning';
        return;
    }

    if (isNaN(sales) && isNaN(transactions)) {
        resultDiv.innerHTML = 'Please enter sales amount or transaction count.';
        resultDiv.className = 'tool-result show warning';
        return;
    }

    const stateData = statesData.find(s => s.abbr === stateAbbr);

    if (!stateData || stateData.nexusThreshold === 'N/A') {
        resultDiv.innerHTML = `${stateData?.name || stateAbbr} does not have sales tax or nexus requirements.`;
        resultDiv.className = 'tool-result show info';
        return;
    }

    const thresholdAmount = parseInt(stateData.nexusThreshold.replace(/[^0-9]/g, ''));
    const thresholdTransactions = stateData.transactionThreshold ? parseInt(stateData.transactionThreshold) : null;

    const salesExceeds = !isNaN(sales) && sales >= thresholdAmount;
    const transactionsExceed = thresholdTransactions && !isNaN(transactions) && transactions >= thresholdTransactions;

    let nexusStatus = '';
    let resultClass = '';

    if (salesExceeds || transactionsExceed) {
        nexusStatus = 'NEXUS THRESHOLD MET';
        resultClass = 'tool-result show warning';
    } else {
        nexusStatus = 'Below Nexus Threshold';
        resultClass = 'tool-result show success';
    }

    resultDiv.innerHTML = `
        <strong>${stateData.name} Nexus Check: ${nexusStatus}</strong><br><br>
        Sales Threshold: ${stateData.nexusThreshold} ${salesExceeds ? '(EXCEEDED)' : ''}<br>
        Your Sales: $${sales ? sales.toLocaleString() : 'N/A'}<br>
        ${thresholdTransactions ? `
        Transaction Threshold: ${thresholdTransactions} ${transactionsExceed ? '(EXCEEDED)' : ''}<br>
        Your Transactions: ${transactions || 'N/A'}<br>
        ` : ''}
        <br><em>Note: This is a simplified check. Consult the tax team for official determination.</em>
    `;
    resultDiv.className = resultClass;
}

function checkTaxability() {
    const category = document.getElementById('productCategory').value;
    const stateAbbr = document.getElementById('taxabilityState').value;

    const resultDiv = document.getElementById('taxabilityResult');

    if (!category || !stateAbbr) {
        resultDiv.innerHTML = 'Please select both a product category and a state.';
        resultDiv.className = 'tool-result show warning';
        return;
    }

    const stateData = statesData.find(s => s.abbr === stateAbbr);
    const categoryRules = taxabilityRules[category];
    const rule = categoryRules[stateAbbr] || categoryRules['default'];

    const categoryNames = {
        'digital-course': 'Digital Courses',
        'software-saas': 'Software/SaaS',
        'ebook': 'eBooks',
        'digital-download': 'Digital Downloads',
        'membership': 'Memberships',
        'consulting': 'Consulting Services'
    };

    let taxableStatus = '';
    let resultClass = '';

    if (rule.taxable === true) {
        taxableStatus = 'TAXABLE';
        resultClass = 'tool-result show warning';
    } else if (rule.taxable === false) {
        taxableStatus = 'EXEMPT';
        resultClass = 'tool-result show success';
    } else {
        taxableStatus = 'VARIES';
        resultClass = 'tool-result show info';
    }

    resultDiv.innerHTML = `
        <strong>${categoryNames[category]} in ${stateData.name}: ${taxableStatus}</strong><br><br>
        ${rule.notes}<br><br>
        ${stateData.rate !== '0.00%' ? `State Tax Rate: ${stateData.rate}<br>` : ''}
        <em>Note: This is general guidance. Specific taxability may depend on product details. Consult the tax team for complex situations.</em>
    `;
    resultDiv.className = resultClass;
}
