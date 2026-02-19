// ==================== FORM VALIDATION ====================

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            input.style.borderColor = '';
        }

        // Email validation
        if (input.type === 'email' && input.value && !validateEmail(input.value)) {
            input.style.borderColor = '#e74c3c';
            isValid = false;
        }
    });

    return isValid;
}

// ==================== AUTO-CLOSE ALERTS ====================

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});

// ==================== FORM SUBMISSION ====================

document.addEventListener('submit', function(e) {
    const form = e.target;
    const formId = form.id;

    // Add loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        // Re-enable after 2 seconds to prevent double submission
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }, 2000);
    }
});

// ==================== PRODUCT QUANTITY VALIDATION ====================

document.querySelectorAll('input[name="quantity"]').forEach(input => {
    input.addEventListener('change', function() {
        const maxQuantity = parseInt(this.max);
        const minQuantity = parseInt(this.min) || 1;
        let value = parseInt(this.value);

        if (value > maxQuantity) {
            this.value = maxQuantity;
        }
        if (value < minQuantity) {
            this.value = minQuantity;
        }
    });
});

// ==================== CALCULATE INSURANCE PREMIUM ====================

const coverageInput = document.querySelector('input[name="coverage_amount"]');
if (coverageInput) {
    coverageInput.addEventListener('input', function() {
        const coverage = parseFloat(this.value) || 0;
        const premium = (coverage * 0.05).toFixed(2);
        
        // Update the info box if it exists
        const infoBox = document.querySelector('.info-box');
        if (infoBox) {
            infoBox.innerHTML = `
                <p><strong>Premium:</strong> $${premium} (5% of coverage amount)</p>
                <p><strong>Coverage Duration:</strong> 1 Year</p>
                <p><strong>Claim Process:</strong> Quick and hassle-free</p>
            `;
        }
    });
}

// ==================== PRODUCT SEARCH/FILTER ====================

function filterProducts(searchTerm) {
    const productCards = document.querySelectorAll('.product-card');
    const term = searchTerm.toLowerCase();

    productCards.forEach(card => {
        const productName = card.querySelector('h4').textContent.toLowerCase();
        const productDesc = card.querySelector('p') ? card.querySelector('p').textContent.toLowerCase() : '';

        if (productName.includes(term) || productDesc.includes(term)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ==================== MODAL FUNCTIONALITY ====================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking outside of it
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// ==================== UTILITY FUNCTIONS ====================

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// ==================== TOAST NOTIFICATIONS ====================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.innerHTML = `
        ${message}
        <button onclick="this.parentElement.style.display='none';">&times;</button>
    `;

    const container = document.querySelector('main');
    if (container) {
        container.insertBefore(toast, container.firstChild);

        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }
}

// ==================== TABLE SORTING ====================

function sortTable(n) {
    const table = document.querySelector('.table');
    if (!table) return;

    let switching = true;
    let shouldSort = true;
    let dir = 'asc';
    let switchcount = 0;

    while (shouldSort) {
        shouldSort = false;
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length - 1; i++) {
            const x = rows[i].getElementsByTagName('td')[n];
            const y = rows[i + 1].getElementsByTagName('td')[n];

            if (dir == 'asc') {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    shouldSort = true;
                    switchcount++;
                    break;
                }
            } else if (dir == 'desc') {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    shouldSort = true;
                    switchcount++;
                    break;
                }
            }
        }
        if (switchcount == 0 && switching == true) {
            dir = 'desc';
            switching = false;
        }
    }
}

// ==================== LOADING SPINNER ====================

function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.innerHTML = '<div style="text-align: center; padding: 2rem;"><p>Loading...</p></div>';
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// ==================== COMMON EVENT LISTENERS ====================

document.addEventListener('DOMContentLoaded', function() {
    // Add active state to current navigation item
    const currentPage = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
        }
    });

    // Initialize tooltips if needed
    initializeTooltips();
});

function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
        });

        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// ==================== EXPORT FUNCTIONS ====================

function exportToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => cell.textContent);
        csv.push(rowData.join(','));
    });

    const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
    const link = document.createElement('a');
    link.setAttribute('href', encodeURI(csvContent));
    link.setAttribute('download', filename);
    link.click();
}

console.log('AgriMarket JavaScript loaded successfully!');
